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
      - images must be "HTML friendly",
    """

    accepted_images = ('.jpg', '.png')

    def add_dest_parser(self, parser):
        """Adds a parser for creating a file formatted for a CodeRunner EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        parser.add_argument('-p', '--penalty',
                            choices=['0, 0, 10, 20, ...', '10, 20, ...',
                                     '0, 0, ...'],
                            default='0, 0, 10, 20, ...', metavar='P',
                            help='Set marking penalty regime. Options are:\
                                 \n\"0, 0, 10, 20, ...\" (default), \
                                 \n\"0, 0, ...\",\n or \"10, 20, ...\"')
        parser.add_argument('-an', '--allornothing', action='store_true',
                            dest='all_or_nothing',
                            help='Set all-or-nothing marking behavior.')
        parser.add_argument('-l', '--language', choices=sorted(list(
                                Evaluation.accepted_sources)),
                            default='c', help='Set programming language.')

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

        def add_solution(evaluation):
            def cr_type(lang):
                if lang == 'c':
                    return 'c_program'
                elif lang == 'cpp':
                    return 'cpp_program'
                elif lang == 'py':
                    return 'python3'
                raise ValueError(f'{lang} source file not supported.')

            for lang, source in evaluation.solutions['main'].items():
                if lang == args.language:
                    root.find('answer').append(CDATA(source))
                    set_text('coderunnertype', cr_type(lang))
                    break
            else:
                for lang, source in evaluation.solutions['accepted'].items():
                    if lang == args.language:
                        root.find('answer').append(CDATA(source))
                        set_text('coderunnertype', cr_type(lang))
                        break
                else:
                    langs = set(l for sols in evaluation.solutions.values()
                                for l in sols.keys())
                    langs = ', '.join(l for l in sorted(langs))
                    raise ValueError(f'No {args.language} solution available.'
                                     f' Try one of [{langs}].')

        def add_tags(statement):
            tags = root.find("tags")
            for tag in statement.tags:
                te = ET.Element('tag')
                ET.SubElement(te, 'text').text = tag
                tags.append(te)

        def append_tests(evaluation):
            def make_test(input, output, is_example):
                xml = os.path.join(cwd, 'test.xml')
                root = ET.parse(xml).getroot()
                root.find("stdin").find("text").text = input
                root.find("expected").find("text").text = output
                root.set("useasexample", '1' if is_example else '0')
                return root

            for key, tests in problem.evaluation.test_cases.items():
                for test in tests.values():
                    t = make_test(test['in'], test['out'], key == 'examples')
                    root.find("testcases").append(t)

        def CDATA(content):
            element = ET.Element('![CDATA[')
            element.text = content
            return element

        def set_questiontext(statement):
            def to_html(header, content):
                html = tex2html(content)
                return f'{header}<p>\n{html}\n</p>\n'

            formats = [('description', ''),
                       ('input', '\n<p>\n<b>Entrada</b><br /></p>\n'),
                       ('output', '\n<p>\n<b>Saída</b><br /></p>\n'),
                       ('notes', '\n<p>\n<b>Observações</b><br /></p>\n')]

            html = '\n'.join(to_html(header, getattr(statement, name))
                             for name, header in formats)

            qt = root.find('questiontext')
            qt.find('text').append(CDATA(html))

            for name, image in statement.images.items():
                if not name.lower().endswith(CodeRunner.accepted_images):
                    raise ValueError(f'Image {name} is not HTML compatible.')

                img = ET.Element('file')
                img.set('name', name)
                img.set('path', '/')
                img.set('encoding', 'base64')
                img.text = str(base64.b64encode(image), 'utf-8')
                qt.append(img)

        def set_text(name, value):
            root.find(name).text = str(value)

        def tex2html(s):
            # Convert the mathematical equations
            s = re.sub(r'\$([^\$]*)\$', r'\\( \1 \\)', s)
            s = re.sub(r'\$\$([^\$]*)\$\$', r'<p><br />\\( \1 \\)<br /></p>', s)

            # Image
            s = re.sub(r'.eps', r'.png', s)
            s = re.sub(r'\\includegraphics\[([^\]]*)\]\{([^\}]*)\}',
                       r'<img src="@@PLUGINFILE@@/\2"><br>', s)

            # Dicts with all the substitution rules for a specific format
            rules1 = {r'\\begin{itemize}': '<ul>',
                      r'\\end{itemize}': '</ul>',
                      r'\\begin{center}': '<p style="text-align: center;">',
                      r'\\end{center}': '</p>',
                      r'\`\`': '\"',
                      r'\'\'': '\"',
                      r'\\arrowvert': '|',
                      r'\\\^': '^',
                      r'\n\n': '</p>\n\n<p>\n'}
            rules2 = {r'\\emph': 'i',
                      r'\\textbf': 'b',
                      r'\\textit': 'i',
                      r'\\texttt': 'tt'}
            rules3 = {r'\\item': 'li'}

            # Apply the rules to the string
            for l, h in rules1.items():
                s = re.sub(l, h, s)

            for l, h in rules2.items():
                l_str = r'%s{([^}]*)}' % l
                h_str = r'<%s>\1</%s>' % (h, h)
                s = re.sub(l_str, h_str, s)

            for l, h in rules3.items():
                l_str = r'%s([^\n]*)' % l
                h_str = r'<%s>\1</%s>' % (h, h)
                s = re.sub(l_str, h_str, s)

            return s

        cwd = os.path.abspath(os.path.dirname(__file__))
        xml = os.path.join(cwd, 'template.xml')
        tree = ET.parse(xml)
        root = tree.getroot()[0]  # question root

        root.find('name').find('text').text = problem.statement.title
        set_questiontext(problem.statement)
        if problem.statement.tutorial:
            root.find('generalfeedback').find(
                'text').text = tex2html(problem.statement.tutorial)

        add_solution(problem.evaluation)
        append_tests(problem.evaluation)
        add_tags(problem.statement)

        set_text('cputimelimitsecs', problem.evaluation.limits['time_sec'])
        set_text('memlimitmb', problem.evaluation.limits['memory_MB'])
        set_text('penaltyregime', args.penalty)
        set_text('allornothing', 1 if args.all_or_nothing else 0)

        tree.write(f'{problem.id}.xml', 'UTF-8')
        #######################################################################
        # CDATA parsing isn't supported natively, so it needs an override.
        ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
        #######################################################################
