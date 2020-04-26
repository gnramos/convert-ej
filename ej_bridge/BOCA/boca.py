#  -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import zipfile

# Import problem.py classes.
import sys
sys.path.append('..')
from problem import Converter


class BOCA(Converter):
    """Class for converting problems to/from BOCA.

    http://bombonera.org/

    BOCA works with zip files in a specific tree structure. This class
    considers a "tex" folder with the Statement info in separate files.
    PDF composition is simplified via boca.sty.
    """

    def add_dest_parser(self, parser):
        """Adds a parser for creating a file formatted for a BOCA EJudge.

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

    def add_origin_parser(self, parser):
        """Adds a parser for creating an EJudgeProblem from a file formatted
        for a BOCA EJudge.

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
                                             f' from {tex_file}.')
                            # try:
                            #     # run again to show errors
                            #     subprocess.check_call(cmd, cwd=args.tmp)
                            # except Exception:
                            #     raise ValueError(f'Unable to create pdf '
                            #                      f'from {tex_file}.tex.')

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

        def add_test_cases():
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

            def write_tags():
                tags = ','.join(tag for tag in problem.statement.tags)
                write('tags', tags, ext='.csv')

            tex_dir = os.path.join(tmpl_dir, 'tex')
            write_tex()
            write_image_files()
            write_tags()

        problem_zip = f'{problem.id}.zip'
        cwd = os.path.abspath(os.path.dirname(__file__))
        tmpl_dir = os.path.join(cwd, 'templates')

        with zipfile.ZipFile(problem_zip, 'w') as pzip:
            add_tex()          # Generates TeX files
            add_description()  # Includes creating the pdf from the TeX files
            add_limits()
            add_test_cases()   # Populates the input/output directories

            processed = ['description', 'input', 'output', 'limits', 'tex']
            with os.scandir(tmpl_dir) as it:
                for entry in it:
                    if entry.is_dir() and entry.name not in processed:
                        add_template(entry.path)
