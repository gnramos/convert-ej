#  -*- coding: utf-8 -*-

import base64
import os
import re
import xml.etree.ElementTree as ET

# Import problem.py classes.
import sys
sys.path.append('..')
from problem import Converter, Evaluation


class CodeRunner(Converter):
    """Class for converting problems to/from CodeRunner.

    https://coderunner.org.nz/

    Keep in mind that:
      - Files from CodeRunner must be exported as "Moodle XML".
      - Images must be "HTML friendly".
      - The question is defined by a single solution's programming language.
      Choosing 'all' for language creates a new file per available solution.
      - Penalties are defined in a 10% growing series, i.e., each wrong attempt
      causes a 10% larges penalty in the question's points.
    """

    accepted = {'images': ('.jpg', '.png'),
                'types': {'c': 'c_program',
                          'cpp': 'cpp_program',
                          'py': 'python3'}}

    def add_dest_parser(self, parser):
        """Adds a parser for creating a file formatted for a CodeRunner EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        def check_penalty(choice):
            choice = int(choice)
            if choice < 0:
                raise ValueError('Penalty {choice} cannot be negative')

            return ', '.join((['0'] * choice) + ['10', '20', '...'])

        parser.add_argument('-p', '--penalty', type=check_penalty,
                            default='2',
                            help='Number of attempts without penalty.'
                            ' (default 2)')
        parser.add_argument('-an', '--allornothing', action='store_true',
                            dest='all_or_nothing',
                            help='Set all-or-nothing marking behavior.')
        parser.add_argument('-l', '--language', choices=sorted(list(
                                CodeRunner.accepted['types'].keys())),
                            default='all', help='Set programming language.')

    def add_origin_parser(self, subparsers):
        """Adds a parser for creating an EJudgeProblem from a file formatted
        for a CodeRunner EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        raise NotImplementedError

    def read(self, file, args):
        """Reads a problem from file and returns it as an EJudgeProblem.

        Keyword arguments:
        file -- the file containing the data for the problem
        args -- the arguments for configuring the EJudgeProblem
        """
        raise NotImplementedError

    def write(self, problem, args):
        """Writes the given EJudgeProblem into a CodeRunner file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the arguments for configuring the created file
        """
        def add_solution(language):
            def find_source(language):
                for solutions in problem.evaluation.solutions:
                    if language in solutions.keys():
                        return solutions[language]

            answer = root.find('answer')
            if answer.getchildren():
                answer.remove(answer.getchildren()[0])

            source = find_source(language)
            answer.append(CDATA(source))
            set_text('coderunnertype', CodeRunner.accepted['types'][language])

        def add_tags():
            tags = root.find("tags")
            for tag in problem.statement.tags:
                te = ET.Element('tag')
                ET.SubElement(te, 'text').text = tag
                tags.append(te)

        def append_tests():
            def make_test(input, output, is_example):
                xml = os.path.join(cwd, 'test.xml')
                root = ET.parse(xml).getroot()
                root.find("stdin").find("text").text = input
                root.find("expected").find("text").text = output
                root.set("useasexample", '1' if is_example else '0')
                return root

            for key, tests in problem.evaluation.tests.items():
                for test in tests.values():
                    t = make_test(test['in'], test['out'], key == 'examples')
                    root.find("testcases").append(t)

        def CDATA(content):
            element = ET.Element('![CDATA[')
            element.text = content
            return element

        def get_languages_from_solutions():
            languages = set(CodeRunner.accepted['types'].keys()
                            if args.language == 'all' else [args.language])
            available = set([k
                            for solutions in problem.evaluation.solutions
                            for k in solutions.keys()])
            return available & languages

        def set_questiontext():
            def to_html(header, content):
                html = tex2html(content).strip()
                header = html_tag(header, 'b')
                return f'<p>\n{header}\n{html}\n</p>\n'

            formats = [('description', ''),
                       ('input', 'Entrada'),
                       ('output', 'Saída'),
                       ('notes', 'Observações')]

            html = '\n'.join(to_html(header, getattr(problem.statement, name))
                             for name, header in formats)

            qt = root.find('questiontext')
            qt.find('text').append(CDATA(html))

            for name, image in problem.statement.images.items():
                if not name.lower().endswith(CodeRunner.accepted['images']):
                    raise ValueError(f'Image {name} is not HTML compatible')

                img = ET.Element('file')
                img.set('name', name)
                img.set('path', '/')
                img.set('encoding', 'base64')
                img.text = str(base64.b64encode(image), 'utf-8')
                qt.append(img)

        def set_text(name, value):
            root.find(name).text = str(value)

        def html_tag(text, tag='', options=''):
            if text and tag:
                if options:
                    options = f' {options}'
                return f'<{tag}{options}>{text}</{tag}>'
            return text

        def tex2html(s):
            def environments(s):
                # Process item before the environment, using \ as end delimiter.
                s = re.sub(r'\\item ([.\s\S]*?)(?=\\)', r'<li>\1</li>\n', s)

                repl = {'itemize': 'ul', 'enumerate': 'ol'}
                for env, t in repl.items():
                    s = re.sub(f'\\\\begin{{{env}}}([.\s\S]*?)\\\\end{{{env}}}',
                               html_tag('\\1', t), s)

                s = re.sub(f'\\\\begin{{center}}([.\s\S]*?)\\\\end{{center}}',
                           html_tag('\\1', 'p', 'style="text-align: center;"'),
                           s)

                return s

            def font(s):
                repl = {'textbf': 'b', 'bf': 'b',
                        'textit': 'i', 'it': 'i', 'emph': 'i',
                        'textrm': None,
                        'texttt': 'tt',
                        't': 'tt'}  # This has issues with nested tags...
                for cmd, t in repl.items():
                    s = re.sub(f'\\\\{cmd}{{(.*?)}}', html_tag('\\1', tag=t), s)
                return s

            def images(s):
                def parse(options):
                    opts = []

                    if options:
                        options = options.lower()

                        pattern = r'scale.*?= *([0-9]*\.?[0-9]+)'
                        m = re.search(pattern, options)
                        if m:
                            width = int(float(m.group(1)) * 100)
                            opts.append(f'width="{width}%"')
                        else:
                            pattern = r'width.*?= *([0-9]*\.?[0-9]+)' \
                                      ' *\\textwidth'
                            m = re.search(pattern, options)
                            if m:
                                width = int(float(m.group(1)) * 100)
                                opts.append(f'width="{width}%"')
                            else:
                                print(f'\tImage {file} has unknown options '
                                      '({options}).')

                    return ' '.join(o for o in opts)

                def check_file(file):
                    if file in problem.statement.images:
                        return file

                    for img in problem.statement.images:
                        if img.startswith(f'{file}.'):
                            return img

                    raise ValueError('Cannot find {file} image')

                pattern = r'\\includegraphics([\[].*[\]])?{(.*?)}'
                for options, file in re.findall(pattern, s):
                    c_file = check_file(file)
                    options = parse(options)

                    pattern = f'\\\\includegraphics.*?{{{file}}}'
                    image = f'src="@@PLUGINFILE@@/{c_file}" {options}'
                    s = re.sub(pattern, html_tag(' ', 'img', image), s)
                return s

            def math(s):
                s = re.sub(r'\$\$(.*?)\$\$', '\\[\\1\\]', s)
                s = re.sub(r'\$([^\$]*)\$', '\\(\\1\\)', s)
                return s

            def text(s):
                s = re.sub(r'``(.*?)\'\'', '"\\1"', s)
                s = re.sub(r'`(.*?)\'', '\'\\1\'', s)
                s = re.sub(r'\n\n', '\n</p>\n<p>\n', s)

                for cmd in re.findall(r'(\\\w+)', s):
                    print(f'\tPossible unformatted TeX command: {cmd}')

                return s

            s = math(s)
            s = font(s)
            s = images(s)
            s = environments(s)
            s = text(s)

            return s

        #######################################################################
        # CDATA parsing isn't supported natively, so it needs an override.
        _serialize_xml = ET._serialize_xml

        def _serialize_xml_with_CDATA(write, elem, qnames, namespaces,
                                      short_empty_elements, **kwargs):
            if elem.tag == '![CDATA[':
                write("\n<{}{}]]>\n".format(elem.tag, elem.text))
            else:
                return _serialize_xml(write, elem, qnames, namespaces,
                                      short_empty_elements, **kwargs)

        ET._serialize_xml = ET._serialize['xml'] = _serialize_xml_with_CDATA
        #######################################################################

        cwd = os.path.abspath(os.path.dirname(__file__))
        xml = os.path.join(cwd, 'template.xml')
        tree = ET.parse(xml)
        root = tree.getroot()[0]  # question root

        languages = get_languages_from_solutions()
        if not languages:
            raise ValueError(f'No {args.language} solution(s) available')

        root.find('name').find('text').text = problem.statement.title
        set_questiontext()
        if problem.statement.tutorial:
            root.find('generalfeedback').find(
                'text').text = tex2html(problem.statement.tutorial.strip())

        append_tests()
        add_tags()

        set_text('cputimelimitsecs', problem.evaluation.limits['time_sec'])
        set_text('memlimitmb', problem.evaluation.limits['memory_MB'])
        set_text('penaltyregime', args.penalty)
        set_text('allornothing', 1 if args.all_or_nothing else 0)

        for lang in languages:
            add_solution(lang)

            file = os.path.join(args.output_dir, f'{problem.id}-{lang}.xml')
            tree.write(file, 'UTF-8')
            print(f'\tCreated {file}.')

        #######################################################################
        # Undo override to handle CDATA.
        ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
        #######################################################################
