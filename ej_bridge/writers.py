#  -*- coding: utf-8 -*-

import base64
import os
import problem
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile


class BOCA(problem.Writer):
    """Class for writing problems to into BOCA format.

    http://bombonera.org/

    Keep in mind that:
      - BOCA works with zip files in a specific tree structure.
      - Template values for most configurations are defined in "templates"
      directory.
      - This class adds a "tex" folder with the tree structure, where Statement
      info is split into separate files.
      - PDF composition is defined in and style are simplified via boca.sty.
    """

    def __init__(self, parser):
        """Adds arguments for creating a file formatted for BOCA e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        parser.add_argument('--tmp', default='/tmp',
                            help='Directory for storing temporary files.'
                            ' (default /tmp)')
        parser.add_argument('-b', '--basename', default=None,
                            help='Basename for problem description.')
        parser.add_argument('--notes', action='store_true',
                            help='Include the notes in the PDF.')
        parser.add_argument('--tutorial', action='store_true',
                            help='Include the tutorial in the PDF.')

    def write(self, problem, args):
        """Writes the given EJudgeProblem into a BOCA file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the arguments for configuring the created file
        """
        def add_description():
            def add_pdf():
                def call_pdflatex():
                    cmd = ['pdflatex', '-halt-on-error', tex_file]
                    with open(os.devnull, 'w') as DEVNULL:
                        try:
                            subprocess.check_call(cmd, cwd=args.tmp,
                                                  stdout=DEVNULL)
                        except subprocess.CalledProcessError:
                            raise ValueError(f'Unable to create pdf'
                                             f' from {tex_file}')
                            # try:
                            #     # run again to show errors
                            #     subprocess.check_call(cmd, cwd=args.tmp)
                            # except Exception:
                            #     raise ValueError(f'Unable to create pdf '
                            #                      f'from {tex_file}.tex')

                tex_file = os.path.join(args.tmp, 'main.tex')
                pdf_file = os.path.join(args.tmp, 'main.pdf')
                call_pdflatex()
                with open(pdf_file, 'rb') as f:
                    pzip.writestr(f'description/{problem.id}.pdf', f.read())

            def add_problem_info():
                basename = args.basename if args.basename else problem.id
                pzip.writestr('description/problem.info',
                              f'basename={basename}\n'
                              f'fullname={problem.statement.title}\n'
                              f'descfile={problem.id}.pdf\n')

            add_problem_info()
            add_pdf()

        def add_limits():
            with os.scandir(os.path.join(tmpl_dir, 'limits')) as it:
                for entry in it:
                    with open(entry.path) as f:
                        limits = [line.rstrip('\r\n')
                                  for line in f.readlines()
                                  if not line.startswith('#')]

                    time_sec = problem.evaluation.limits['time_sec']
                    memory_MB = problem.evaluation.limits['memory_MB']
                    limits[0] = f'echo {time_sec}'
                    # limits[1] = f'echo {num_repetitions}'
                    limits[2] = f'echo {memory_MB}'
                    # limits[3] = f'echo {max_file_size_KB}'

                    pzip.writestr(f'limits/{entry.name}', '\n'.join(limits))

        def add_template(dir_path):
            with os.scandir(dir_path) as it:
                dir_name = os.path.split(dir_path)[-1]
                for entry in it:
                    with open(entry.path, 'rb') as template:
                        with pzip.open(f'{dir_name}/{entry.name}', 'w') as f:
                            f.write(template.read())

        def add_tests():
            for key, tests in problem.evaluation.tests.items():
                for name, files in tests.items():
                    for k, data in files.items():
                        pzip.writestr(f'{k}put/{name}', data)

        def add_tex():
            def write(name, content, mode='w', ext='.tex'):
                # To temporary dir.
                file = os.path.join(args.tmp, f'{name}{ext}')
                with open(file, mode) as f:
                    f.write(content)

                # To the zip.
                file = os.path.join('tex', f'{name}{ext}')
                pzip.writestr(file, content)

            def write_image_files():
                for name, img in problem.statement.images.items():
                    write(name, img, mode='wb', ext='')

            def write_tags():
                tags = ','.join(tag for tag in problem.statement.tags)
                write('tags', tags, ext='.csv')

            def write_tex():
                def write_examples(examples):
                    def table(num_rows):
                        def cell(file):
                            return f'\\vspace{{-1.2\\baselineskip}}%\n' \
                                   f'\\verbatiminput{{{file}}}%\n' \
                                   f'\\vspace*{{-2\\baselineskip}}'

                        def cells(i):
                            return '\n&\n'.join(cell(f'{i:02}{ext}')
                                                for ext in ('.in', '.out'))

                        header = f'\\textbf{{Input}} & \\textbf{{Output}}%'
                        end = '\n\\\\\\hline%\n'
                        rows = end.join(cells(i)
                                        for i in range(1, num_rows + 1))

                        col = 'p{.5\\textwidth}'

                        return f'\\noindent%\n' \
                               f'\\begin{{tabular}}[t]' \
                               f'{{|{col}|{col}|}}%\n' \
                               f'\\hline%\n' \
                               f'{header}{end}' \
                               f'{rows}{end}' \
                               f'\\end{{tabular}}%'

                    for i in range(len(examples)):
                        write(f'{i+1:02}', examples[i]['in'], ext='.in')
                        write(f'{i+1:02}', examples[i]['out'], ext='.out')

                    write('examples', table(len(examples)))

                def write_main():
                    main = os.path.join(tex_dir, 'main.tex')
                    with open(main) as f:
                        tex = f.read()
                        if not (args.notes and problem.statement.notes):
                            tex.replace('\\inputNotes%\n', '')
                        if not (args.tutorial and
                                problem.statement.tutorial):
                            tex.replace('\\inputTutorial%\n', '')

                        write('main', tex)

                style = os.path.join(tex_dir, 'boca.sty')
                shutil.copy(style, args.tmp)

                write('title', problem.statement.title)
                write('description', problem.statement.description)
                write('input', problem.statement.input)
                write('output', problem.statement.output)
                write_examples(problem.statement.examples)
                write('notes', problem.statement.notes)
                write('tutorial', problem.statement.tutorial)
                write_main()

            tex_dir = os.path.join(tmpl_dir, 'tex')
            write_tex()
            write_image_files()
            write_tags()

        problem_zip = os.path.join(args.output_dir, f'{problem.id}.zip')
        cwd = os.path.abspath(os.path.dirname(__file__))
        tmpl_dir = os.path.join(cwd, 'templates', 'BOCA')

        with zipfile.ZipFile(problem_zip, 'w') as pzip:
            add_tex()          # Generates TeX files
            add_description()  # Also creates the pdf from the TeX files
            add_limits()
            add_tests()        # Populates the input/output directories

            processed = ['description', 'input', 'output', 'limits', 'tex']
            with os.scandir(tmpl_dir) as it:
                for entry in it:
                    if entry.is_dir() and entry.name not in processed:
                        add_template(entry.path)


class CodeRunner(problem.Writer):
    """Class for writing problems to into CodeRunner format.

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

    def __init__(self, parser):
        """Adds arguments for creating a file formatted for CodeRunner e-judge.

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
                xml = os.path.join(cwd, 'templates', 'CodeRunner', 'test.xml')
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

                no_math = re.sub(r'(\\[\(\[].*?\\[\)\]])', '', s)
                for cmd in re.findall(r'(\\\w+)', no_math):
                    print(f'\tPossible unformatted TeX command: {cmd}')

                return s

            s = math(s)
            s = font(s)
            s = images(s)
            s = environments(s)
            s = text(s)  # must be processed after "math"

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
        xml = os.path.join(cwd, 'templates', 'CodeRunner', 'problem.xml')
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
