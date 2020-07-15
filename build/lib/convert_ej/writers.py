#  -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import base64
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile


class Writer(ABC):
    """Abstract class for writing an E-judge problem."""
    @abstractmethod
    def _write_aux_files(self):
        pass

    @abstractmethod
    def _write_description(self):
        pass

    @abstractmethod
    def _write_examples(self):
        pass

    @abstractmethod
    def _write_id(self):
        pass

    @abstractmethod
    def _write_input(self):
        pass

    @abstractmethod
    def _write_output(self):
        pass

    @abstractmethod
    def _write_limits(self):
        pass

    @abstractmethod
    def _write_notes(self):
        pass

    @abstractmethod
    def _write_solutions(self):
        pass

    @abstractmethod
    def _write_tags(self):
        pass

    @abstractmethod
    def _write_tests(self):
        pass

    @abstractmethod
    def _write_title(self):
        pass

    @abstractmethod
    def _write_tutorial(self):
        pass

    def write(self, problem, output_dir='./'):
        """Writes an Problem to a file."""
        self.problem = problem
        self.output_dir = output_dir

        self._write_id()
        self._write_title()
        self._write_description()
        self._write_input()
        self._write_output()
        self._write_examples()
        self._write_aux_files()
        self._write_tags()
        self._write_tutorial()
        self._write_notes()
        self._write_tests()
        self._write_solutions()
        self._write_limits()


class BOCA(Writer):
    """Writes an E-judge problem in BOCA format."""
    def _write(self, name, content, mode='w', ext='.tex'):
        # To temporary dir.
        file = os.path.join(self.tmp_tex_dir, f'{name}{ext}')
        with open(file, mode) as f:
            f.write(content)

        # To the zip.
        file = os.path.join('tex', f'{name}{ext}')
        self.pzip.writestr(file, content)

    def _write_aux_files(self):
        def aux_files():
            for name, file in self.problem.statement.aux_files.items():
                self._write(name, file, mode='wb', ext='')

        def template_dirs():
            def write_tmpl(dir_path):
                with os.scandir(dir_path) as it:
                    dir_name = os.path.split(dir_path)[-1]
                    for entry in it:
                        with open(entry.path, 'rb') as template:
                            with self.pzip.open(f'{dir_name}/{entry.name}', 'w') as f:
                                f.write(template.read())

            with os.scandir(self.template_dir) as it:
                for entry in it:
                    if entry.is_dir() and entry.name not in ['limits', 'tex']:
                        write_tmpl(entry.path)
        aux_files()
        template_dirs()

    def _write_description(self):
        self._write('description', self.problem.statement.description)

    def _write_examples(self):
        examples = []
        # Write examples to temporary dir
        os.mkdir(os.path.join(self.tmp_dir, 'input'))
        os.mkdir(os.path.join(self.tmp_dir, 'output'))
        for e, io in self.problem.evaluation.tests['examples'].items():
            examples.append(e)
            for key, value in io.items():
                file = os.path.join(self.tmp_dir, f'{key}put', e)
                with open(file, 'w') as f:
                    f.write(value)

        # Write list to TeX
        self._write('examples', ','.join(examples), ext='.csv')

    def _write_id(self):
        self.pzip.writestr('description/problem.info',
                           f'basename={self.problem.id}\n'
                           f'fullname={self.problem.statement.title}\n'
                           f'descfile={self.problem.id}.pdf\n')

    def _write_input(self):
        self._write('input', self.problem.statement.input)

    def _write_output(self):
        self._write('output', self.problem.statement.output)

    def _write_limits(self):
        self._write('time_limit', str(self.problem.evaluation.limits['time_sec']))

        with os.scandir(os.path.join(self.template_dir, 'limits')) as it:
            for entry in it:
                with open(entry.path) as f:
                    limits = [line.rstrip('\r\n')
                              for line in f.readlines()
                              if not line.startswith('#')]

                time_sec = self.problem.evaluation.limits['time_sec']
                memory_MB = self.problem.evaluation.limits['memory_MB']
                maxfilesize_KB = self.problem.evaluation.limits['maxfilesize_KB']
                limits[0] = f'echo {time_sec}'
                # limits[1] = f'echo {num_repetitions}'
                limits[2] = f'echo {memory_MB}'
                limits[3] = f'echo {maxfilesize_KB}'

                self.pzip.writestr(f'limits/{entry.name}', '\n'.join(limits))

    def _write_notes(self):
        self._write('notes', self.problem.statement.notes)

    def _write_pdf(self, options):
        def call_pdflatex(tex_file):
            cmd = ['pdflatex', '-halt-on-error', tex_file]
            with open(os.devnull, 'w') as DEVNULL:
                try:
                    subprocess.check_call(cmd, cwd=self.tmp_tex_dir,
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

        def write_templates():
            with os.scandir(self.template_tex_dir) as it:
                for entry in it:
                    if entry.is_file and not entry.name.startswith(('.', 'main.tex')):
                        with open(entry.path) as tmpl_file:
                            self._write(entry.name, tmpl_file.read(), ext='')

        def write_main():
            with open(os.path.join(self.template_tex_dir, 'main.tex')) as f:
                main = f.read()
                main = main.replace('documentclass',
                                    f'documentclass[{options}]')
                self._write('main', main)

        write_templates()
        write_main()
        call_pdflatex(os.path.join(self.tmp_tex_dir, 'main.tex'))
        with open(os.path.join(self.tmp_tex_dir, 'main.pdf'), 'rb') as f:
            self.pzip.writestr(f'description/{self.problem.id}.pdf',
                               f.read())

    def _write_solutions(self):
        sol = self.problem.evaluation.solutions
        for ext, solution in sol[0].items():
            self.pzip.writestr(f'solutions/main.{ext}', solution)
        for ext, solution in sol[1].items():
            self.pzip.writestr(f'solutions/accepted.{ext}', solution)

    def _write_tags(self):
        self.pzip.writestr('description/tags.csv',
                           ','.join(tag for tag in self.problem.statement.tags))

    def _write_tests(self):
        num_tests = sum(len(tests)
                        for tests in self.problem.evaluation.tests.values())
        num_digits = len(str(num_tests))
        for tests in self.problem.evaluation.tests.values():
            for name, files in tests.items():
                for io, data in files.items():
                    self.pzip.writestr(f'{io}put/{int(name):0{num_digits}}', data)

    def _write_title(self):
        self._write('title', self.problem.statement.title)

    def _write_tutorial(self):
        self._write('tutorial', self.problem.statement.tutorial)

    def write(self, problem, output_dir='./', tmp_dir='/tmp', add_notes=True,
              add_tutorial=False):
        """Writes the given Problem into a BOCA file.

        http://bombonera.org/

        Keep in mind that:
          - BOCA works with zip files in a specific tree structure.
          - Template values for most configurations are defined in "templates"
          directory.
          - This adds to the tree structure:
            - "/description/tags.csv" for listing keywords describing the problem.
            - "/solutions/" to store source code solutions to the problem; and
            - "/tex/" where Statement info split into separate files.
          - The composition of PDF is defined in main.tex file, "Notes" and
          "Tutorial" are included in the class options. Any necessary auxililary
          files (like images) should be in that directory.

        Keyword arguments:
        problem -- the Problem containing the data for the problem
        output_dir -- the directory to write the file created
        tmp_dir -- the directory to write temporary files, if necessary
        add_notes -- boolean to include (or not) the "notes" in the PDF file
        add_tutorial -- boolean to include (or not) the "tutorial" in the PDF
                        file
        """
        # Setup
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        self.tmp_dir = os.path.join(tmp_dir, problem.id)
        if os.path.isdir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        os.mkdir(self.tmp_dir)
        self.tmp_tex_dir = os.path.join(self.tmp_dir, 'tex')
        os.mkdir(self.tmp_tex_dir)

        class_options = []
        if add_notes and problem.statement.notes:
            class_options.append('notes')
        if add_tutorial and problem.statement.tutorial:
            class_options.append('tutorial')

        # Processing
        problem_zip = os.path.join(output_dir, f'{problem.id}.zip')
        cwd = os.path.abspath(os.path.dirname(__file__))
        self.template_dir = os.path.join(cwd, 'templates', 'BOCA')
        self.template_tex_dir = os.path.join(self.template_dir, 'tex')

        with zipfile.ZipFile(problem_zip, 'w') as pzip:
            self.pzip = pzip
            super().write(problem, output_dir=output_dir)
            self._write_pdf(','.join(class_options))

        # Cleanup
        shutil.rmtree(self.tmp_dir)

        print(f'\tCreated {problem_zip}.')


class CodeRunner(Writer):
    """Writes an E-judge problem in CodeRunner format.

    https://coderunner.org.nz/

    Keep in mind that:
      - Files from CodeRunner must be exported as "Moodle XML".
      - Images must be "HTML friendly".
      - The question is defined by a single solution's programming language.
      Choosing 'all' for language creates a new file per available solution.
      - Penalties are defined in a 10% growing series, i.e., each wrong attempt
      causes a 10% larges penalty in the question's points.
    """

    # Define accepted file types for dealing with CodeRunner.
    FILES = {'source': {'c': 'c_program',
                        'cpp': 'cpp_program',
                        'py': 'python3'},
             'raster images': ('jpeg', 'jpg', 'gif', 'png')}

    def __init__(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        template_path = os.path.join(cwd, 'templates', 'CodeRunner')
        self.problem_xml = os.path.join(template_path, 'problem.xml')
        self.test_xml = os.path.join(template_path, 'test.xml')

    def _add_solution(self, src_lang):
        def find_source(lang):
            for solutions in self.problem.evaluation.solutions:
                if lang in solutions.keys():
                    return solutions[lang]
            raise ValueError(f'No {lang} solution')

        answer = self.root.find('answer')
        for a in answer:
            answer.remove(a)

        source = find_source(src_lang)
        answer.append(self._CDATA(source))
        self._set_text('coderunnertype', CodeRunner.FILES['source'][src_lang])

    def _CDATA(self, content):
        # Handle the CDEnd string "]]>".
        content = re.sub(r']]>', r']]&gt;', content)
        # Include the CDATA tag on the element.
        element = ET.Element('![CDATA[')
        element.text = content
        return element

    def _html_tag(self, text, tag='', options=''):
        if text and tag:
            if options:
                options = f' {options}'
            return f'<{tag}{options}>{text}</{tag}>'
        return text

    def _set_languages(self, src_lang, solutions):
        languages = set(CodeRunner.FILES['source'].keys()
                        if src_lang == 'all' else [src_lang])
        available = set([k
                        for sol in solutions
                        for k in sol.keys()])
        return available & languages

    def _set_text(self, name, value):
        self.root.find(name).text = str(value)

    def _tex2html(self, s):
        def environments(s):
            # Process item before the environment, using \ as end delimiter.
            s = re.sub(r'\\item ([.\s\S]*?)(?=\\)', r'<li>\1</li>\n', s)

            repl = {'itemize': 'ul', 'enumerate': 'ol'}
            for env, t in repl.items():
                s = re.sub(f'\\\\begin{{{env}}}([.\s\S]*?)\\\\end{{{env}}}',
                           self._html_tag('\\1', t), s)

            s = re.sub(f'\\\\begin{{center}}([.\s\S]*?)\\\\end{{center}}',
                       self._html_tag('\\1', 'p', 'style="text-align: center;"'),
                       s)

            return s

        def font(s):
            repl = {'textbf': 'b', 'bf': 'b',
                    'textit': 'i', 'it': 'i', 'emph': 'i',
                    'textrm': None,
                    'texttt': 'tt',
                    't': 'tt'}  # This has issues with nested tags...
            for cmd, t in repl.items():
                s = re.sub(f'\\\\{cmd}{{(.*?)}}', self._html_tag('\\1', tag=t), s)
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
                if file in self.problem.statement.aux_files:
                    return file

                # Extension may have been omitted
                for img in self.problem.statement.aux_files:
                    if img.startswith(f'{file}.'):
                        return img

                raise ValueError('Cannot find {file} image')

            pattern = r'\\includegraphics([\[].*[\]])?{(.*?)}'
            for options, file in re.findall(pattern, s):
                c_file = check_file(file)
                options = parse(options)

                pattern = f'\\\\includegraphics.*?{{{file}}}'
                image = f'src="@@PLUGINFILE@@/{c_file}" {options}'
                s = re.sub(pattern, self._html_tag(' ', 'img', image), s)
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

    def _write_aux_files(self):
        for name, data in self.problem.statement.aux_files.items():
            if name.lower().endswith(CodeRunner.FILES['raster images']):
                img = ET.Element('file')
                img.set('name', name)
                img.set('path', '/')
                img.set('encoding', 'base64')
                img.text = str(base64.b64encode(data), 'utf-8')
                self.root.find('questiontext').append(img)

    def _write_description(self):
        def to_html(header, content):
            html = self._tex2html(content).strip()
            header = self._html_tag(header, 'b')
            return f'<p>\n{header}\n<br>\n{html}\n</p>\n'

        formats = [('description', ''),
                   ('input', 'Entrada'),
                   ('output', 'Saída')]

        if self.problem.statement.notes:
            formats.append(('notes', 'Observações'))

        html = '\n'.join(to_html(header, getattr(self.problem.statement, name))
                         for name, header in formats)

        self.root.find('questiontext').find('text').append(self._CDATA(html))

    def _write_examples(self):
        # Done in _write_tests
        pass

    def _write_id(self):
        # Unecessary
        pass

    def _write_input(self):
        # Done in _write_description
        pass

    def _write_output(self):
        # Done in _write_description
        pass

    def _write_limits(self):
        self._set_text('cputimelimitsecs', self.problem.evaluation.limits['time_sec'])
        self._set_text('memlimitmb', self.problem.evaluation.limits['memory_MB'])
        self._set_text('maxfilesize', self.problem.evaluation.limits['maxfilesize_KB'])

    def _write_notes(self):
        # Done in _write_description
        pass

    def _write_solutions(self):
        # Since there is a file for each language, solutions are written in a
        # loop in "write", using _add_solution.
        pass

    def _write_tags(self):
        tags = self.root.find("tags")
        for tag in self.problem.statement.tags:
            te = ET.Element('tag')
            ET.SubElement(te, 'text').text = tag
            tags.append(te)

    def _write_tests(self):
        def use_as_example(key):
            return '1' if key == 'examples' else '0'

        def set_test(test, key):
            xml = os.path.join(self.test_xml)
            root = ET.parse(xml).getroot()
            root.find("stdin").find("text").text = test['in']
            root.find("expected").find("text").text = test['out']
            root.set("useasexample", use_as_example(key))
            return root

        for key, tests in self.problem.evaluation.tests.items():
            for case in tests.values():
                self.root.find("testcases").append(set_test(case, key))

    def _write_title(self):
        self.root.find('name').find('text').text = self.problem.statement.title

    def _write_tutorial(self):
        if self.problem.statement.tutorial:
            tutorial = self._tex2html(self.problem.statement.tutorial.strip())
            self.root.find('generalfeedback').find('text').text = tutorial

    def write(self, problem, output_dir='./', src_lang='all',
              all_or_nothing=False, penalty_after=2):
        """Writes the given Problem into a CodeRunner file.

        Keyword arguments:
        problem -- the Problem containing the data for the problem
        output_dir -- the directory to write the file created
        src_lang -- the specific language to create a file
        all_or_nothing -- boolean defining the all-or-nothing marking behavior
        penalty_after -- start the penalty regime (10% per mistake) after this
                         number of attempts
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

        # Parse arguments #####################################################
        languages = self._set_languages(src_lang, problem.evaluation.solutions)
        if not languages:
            raise ValueError(f'No {src_lang} solution(s) available')

        if penalty_after < 0:
            raise ValueError(f'Penalty {penalty_after} cannot be negative')
        #######################################################################

        tree = ET.parse(self.problem_xml)
        self.root = tree.getroot()[0]  # question root

        super().write(problem, output_dir=output_dir)

        self._set_text('allornothing', 1 if all_or_nothing else 0)

        penalty_regime = ', '.join((['0'] * penalty_after) + ['10', '20', '...'])
        self._set_text('penaltyregime', penalty_regime)

        for lang in languages:
            self._add_solution(lang)

            file = os.path.join(output_dir, f'{problem.id}-{lang}.xml')
            tree.write(file, 'UTF-8')
            print(f'\tCreated {file}.')

        self.root = None

        #######################################################################
        # Undo override to handle CDATA.
        ET._serialize_xml = ET._serialize['xml'] = _serialize_xml
        #######################################################################
