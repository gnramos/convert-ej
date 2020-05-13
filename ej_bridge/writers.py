#  -*- coding: utf-8 -*-

import base64
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile


def boca(problem, output_dir='./', tmp_dir='/tmp', basename=None,
         add_notes=True, add_tutorial=False):
    """Writes the given EJudgeProblem into a BOCA file.

    http://bombonera.org/

    Keep in mind that:
      - BOCA works with zip files in a specific tree structure.
      - Template values for most configurations are defined in "templates"
      directory.
      - This class adds a "tex" folder with the tree structure, where Statement
      info is split into separate files.
      - The composition of PDF is defined in main.tex file, "Notes" and
      "Tutorial" are included in the class options. Any necessary auxililary
      files should be in that directory.

    Keyword arguments:
    problem -- the EJudgeProblem containing the data for the problem
    output_dir -- the directory to write the file created
    tmp_dir -- the directory to write temporary files, if necessary
    basename -- the basename for problem info
    add_notes -- boolean to include (or not) the "notes" in the PDF file
    add_tutorial -- boolean to include (or not) the "tutorial" in the PDF
                    file
    """
    def add_description_dir():
        def add_pdf():
            def call_pdflatex():
                cmd = ['pdflatex', '-halt-on-error', tex_file]
                with open(os.devnull, 'w') as DEVNULL:
                    try:
                        subprocess.check_call(cmd, cwd=tmp_tex_dir,
                                              stdout=DEVNULL)
                    except subprocess.CalledProcessError:
                        raise ValueError(f'Unable to create pdf'
                                         f' from {tex_file}')
                        # try:
                        #     # run again to show errors
                        #     subprocess.check_call(cmd, cwd=tmp_tex_dir)
                        # except Exception:
                        #     raise ValueError(f'Unable to create pdf '
                        #                      f'from {tex_file}.tex')

            tex_file = os.path.join(tmp_tex_dir, 'main.tex')
            call_pdflatex()
            with open(os.path.join(tmp_tex_dir, 'main.pdf'), 'rb') as f:
                pzip.writestr(f'description/{problem.id}.pdf', f.read())

        def add_problem_info():
            pzip.writestr('description/problem.info',
                          f'basename={problem.id}\n'
                          f'fullname={problem.statement.title}\n'
                          f'descfile={problem.id}.pdf\n')

        add_problem_info()
        add_pdf()

    def add_IO_dirs():
        num_tests = sum(len(tests) for tests in problem.evaluation.tests.values())
        num_digits = len(str(num_tests))
        for tests in problem.evaluation.tests.values():
            for name, files in tests.items():
                for io, data in files.items():
                    pzip.writestr(f'{io}put/{int(name):0{num_digits}}', data)

    def add_limits_dir():
        with os.scandir(os.path.join(template_dir, 'limits')) as it:
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

    def add_other_dirs(exceptions):
        def add_dir(dir_path):
            with os.scandir(dir_path) as it:
                dir_name = os.path.split(dir_path)[-1]
                for entry in it:
                    with open(entry.path, 'rb') as template:
                        with pzip.open(f'{dir_name}/{entry.name}', 'w') as f:
                            f.write(template.read())

        with os.scandir(template_dir) as it:
            for entry in it:
                if entry.is_dir() and entry.name not in exceptions:
                    add_dir(entry.path)


    def add_tex_dir():
        def write(name, content, mode='w', ext='.tex'):
            # To temporary dir.
            file = os.path.join(tmp_tex_dir, f'{name}{ext}')
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
            def write_examples():
                examples = []
                # Write examples to temporary dir
                os.mkdir(os.path.join(tmp_dir, 'input'))
                os.mkdir(os.path.join(tmp_dir, 'output'))
                for e, io in problem.evaluation.tests['examples'].items():
                    examples.append(e)
                    for key, value in io.items():
                        file = os.path.join(tmp_dir, f'{key}put', e)
                        with open(file, 'w') as f:
                            f.write(value)

                # Write list to TeX
                write('examples', ','.join(examples), ext='.csv')

            def write_main():
                notes = 'notes' if add_notes and problem.statement.notes else ''
                tutorial = 'tutorial' if add_tutorial and problem.statement.tutorial else ''

                with open(os.path.join(template_tex_dir, 'main.tex')) as f:
                    main = f.read()
                    if notes or tutorial:
                        main = main.replace('documentclass',
                            f'documentclass[{notes},{tutorial}]')
                    write('main', main)

            write('title', problem.statement.title)
            write('time_limit', str(problem.evaluation.limits['time_sec']))
            write('description', problem.statement.description)
            write('input', problem.statement.input)
            write('output', problem.statement.output)
            write_examples()
            write('notes', problem.statement.notes)
            write('tutorial', problem.statement.tutorial)
            write_main()

        template_tex_dir = os.path.join(template_dir, 'tex')

        with os.scandir(template_tex_dir) as it:
            for entry in it:
                if entry.is_file and not entry.name.startswith(('.', 'main.tex')):
                    with open(entry.path) as template:
                        write(entry.name, template.read(), ext='')

        write_tex()
        write_image_files()
        write_tags()

    # Setup
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_dir = os.path.join(tmp_dir, problem.id)
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    tmp_tex_dir = os.path.join(tmp_dir, 'tex')
    os.mkdir(tmp_tex_dir)

    # Processing
    problem_zip = os.path.join(output_dir, f'{problem.id}.zip')
    cwd = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(cwd, 'templates', 'BOCA')

    with zipfile.ZipFile(problem_zip, 'w') as pzip:
        add_tex_dir()          # Generates TeX files
        add_description_dir()  # Also creates the pdf from the TeX files
        add_limits_dir()
        add_IO_dirs()          # Populates the input/output directories
        add_other_dirs(exceptions=['limits', 'tex'])

    # Cleanup
    shutil.rmtree(tmp_dir)


# Define accepted image and source code file types for dealing with CodeRunner.
CODERUNNER = {'images': ('.jpg', '.png'),
              'types': {'c': 'c_program',
                        'cpp': 'cpp_program',
                        'py': 'python3'}}


def coderunner(problem, output_dir='./', src_lang='all',
               all_or_nothing=False, penalty_after=2):
    """Writes the given EJudgeProblem into a CodeRunner file.

    https://coderunner.org.nz/

    Keep in mind that:
      - Files from CodeRunner must be exported as "Moodle XML".
      - Images must be "HTML friendly".
      - The question is defined by a single solution's programming language.
      Choosing 'all' for language creates a new file per available solution.
      - Penalties are defined in a 10% growing series, i.e., each wrong attempt
      causes a 10% larges penalty in the question's points.

    Keyword arguments:
    problem -- the EJudgeProblem containing the data for the problem
    output_dir -- the directory to write the file created
    src_lang -- the specific language to create a file
    all_or_nothing -- boolean defining the all-or-nothing marking behavior
    penalty_after -- start the penalty regime (10% per mistake) after this
                     number of attempts
    """
    def add_solution(src_lang):
        def find_source(lang):
            for solutions in problem.evaluation.solutions:
                if lang in solutions.keys():
                    return solutions[lang]
            raise ValueError(f'No {lang} solution')

        answer = root.find('answer')
        if answer.getchildren():
            answer.remove(answer.getchildren()[0])

        source = find_source(src_lang)
        answer.append(CDATA(source))
        set_text('coderunnertype', CODERUNNER['types'][src_lang])

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
        languages = set(CODERUNNER['types'].keys()
                        if src_lang == 'all' else [src_lang])
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
            if not name.lower().endswith(CODERUNNER['images']):
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

    # Parse arguments #####################################################
    languages = get_languages_from_solutions()
    if not languages:
        raise ValueError(f'No {src_lang} solution(s) available')

    if penalty_after < 0:
        raise ValueError(f'Penalty {penalty_after} cannot be negative')
    #######################################################################

    cwd = os.path.abspath(os.path.dirname(__file__))
    xml = os.path.join(cwd, 'templates', 'CodeRunner', 'problem.xml')
    tree = ET.parse(xml)
    root = tree.getroot()[0]  # question root

    root.find('name').find('text').text = problem.statement.title
    set_questiontext()
    if problem.statement.tutorial:
        root.find('generalfeedback').find(
            'text').text = tex2html(problem.statement.tutorial.strip())

    append_tests()
    add_tags()

    set_text('cputimelimitsecs', problem.evaluation.limits['time_sec'])
    set_text('memlimitmb', problem.evaluation.limits['memory_MB'])
    set_text('allornothing', 1 if all_or_nothing else 0)

    penalty_regime = ', '.join((['0'] * penalty_after) + ['10', '20', '...'])
    set_text('penaltyregime', penalty_regime)

    for lang in languages:
        add_solution(lang)

        file = os.path.join(output_dir, f'{problem.id}-{lang}.xml')
        tree.write(file, 'UTF-8')
        print(f'\tCreated {file}.')

    #######################################################################
    # Undo override to handle CDATA.
    ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
    #######################################################################
