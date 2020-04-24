#  -*- coding: utf-8 -*-

import os
import subprocess
import zipfile

# Import problem.py classes.
import sys
sys.path.append('..')
from problem import Converter


class BOCA(Converter):
    """Class for converting problems to/from BOCA.

    http://bombonera.org/

    Files from BOCA must be in the zip format.
    """

    def add_dest_parser(self, parser):
        """Adds a parser for creating a file formatted for a BOCA EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        parser.add_argument('--tmp', default='/tmp',
                            help='Directory for storing temporary files.'
                            ' (default /tmp')
        parser.add_argument('-b', '--basename', default=None,
                            help='Basename for problem description.')

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
                def write_image_files():
                    for name, img in problem.statement.images.items():
                        # To file, so the PDF can be generated.
                        with open(os.path.join(args.tmp, name), 'wb') as f:
                            f.write(img)

                        # To the zip.
                        zip_obj.writestr(os.path.join('tex', name), img)

                def write_pdf():
                    def pdflatex():
                        env = os.environ.copy()
                        env['TEXINPUTS'] = f'.:{args.tmp}//:'
                        cmd = ['pdflatex', '-output-directory=' + args.tmp,
                               '-interaction=nonstopmode', '-halt-on-error',
                               tex_file]
                        with open(os.devnull, 'w') as DEVNULL:
                            try:
                                subprocess.check_call(cmd, env=env, stdout=DEVNULL)
                            except subprocess.CalledProcessError:
                                raise ValueError(f'Unable to create pdf from'
                                                 f' {tex_file}.')
                                # try:
                                #     # run again to show errors
                                #     subprocess.check_call(cmd, env=env)
                                # except Exception as e:
                                #     raise ValueError(f'Unable to create pdf'
                                #                      f' from {tex_file}.')

                    pdflatex()

                    pdf_file = tex_file.replace('.tex', '.pdf')
                    with open(pdf_file, 'rb') as f:
                        pdf = f.read()

                    zip_obj.writestr(f'description/{problem.id}.pdf', pdf)

                def write_tex():
                    def table(examples):
                        def rows():
                            def verbatim(ex):
                                return f'\\vspace{{-1.2\\baselineskip}}%\n' \
                                       f'\\begin{{verbatim}}\n' \
                                       f'{ex}\\end{{verbatim}}\n' \
                                       f'\\vspace*{{-2\\baselineskip}}%'

                            def row(ex_in, ex_out):
                                return f'{verbatim(ex_in)}\n&' \
                                       f'\n{verbatim(ex_out)}'

                            return [row(ex['in'], ex['out']) for ex in examples]

                        header = r'\textbf{Input} & \textbf{Output}'
                        lines = [header] + rows()
                        table = '\n\\\\\\hline%\n'.join(l for l in lines)
                        return '\\noindent%\n' \
                               '\\begin{tabular}[t]' \
                               '{|p{.5\\textwidth}|p{.5\\textwidth}|}%\n' \
                               '\\hline%\n' \
                               f'{table}' \
                               '\n\\end{tabular}%'

                    def replace(name, content):
                        return tex.replace(f'%<{name}>%\n%</{name}>%',
                                           f'%<{name}>%\n{content}\n%</{name}>%')

                    def section(name, content):
                        return replace(name,
                                       f'\\textbf{{{name.capitalize()}}}%\n'
                                       f'{content}')

                    def title(text):
                        return f'\\begin{{center}}%\n' \
                               f'\\LARGE\\textbf{{{text}}}%\n' \
                               f'\\end{{center}}%'

                    with open(os.path.join(cwd, 'templates',
                                           'description.tex')) as f:
                        tex = f.read()

                    stmt = problem.statement
                    tex = replace('TITLE', title(stmt.title))
                    tex = replace('DESCRIPTION', stmt.description)
                    tex = section('INPUT', stmt.input)
                    tex = section('OUTPUT', stmt.output)
                    tex = section('EXAMPLES', table(stmt.examples))
                    if stmt.notes:
                        tex = replace('NOTES', stmt.notes)

                    # To file, so the PDF can be generated.
                    with open(tex_file, 'w') as f:
                        f.write(tex)

                    # To the zip.
                    zip_obj.writestr(os.path.join('tex', f'{problem.id}.tex'),
                                     tex)

                tex_file = os.path.join(args.tmp, f'{problem.id}.tex')
                write_tex()
                write_image_files()
                write_pdf()

            def add_problem_info():
                basename = args.basename if args.basename else problem.id
                zip_obj.writestr('description/problem.info',
                                 f'basename={basename}\n'
                                 f'fullname={problem.statement.title}\n'
                                 f'descfile={problem.id}.pdf\n')

            add_pdf()
            add_problem_info()

        def add_IO():
            for key, tests in problem.evaluation.test_cases.items():
                for name, files in tests.items():
                    for k, data in files.items():
                        zip_obj.writestr(f'{k}put/{name}', data)

        def add_limits():
            with os.scandir(os.path.join(cwd, 'templates', 'zip',
                                         'limits')) as it:
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

                    zip_obj.writestr(f'limits/{entry.name}', '\n'.join(limits))

        def add_template(dir_path):
            with os.scandir(dir_path) as it:
                dir_name = os.path.split(dir_path)[-1]
                for entry in it:
                    with open(entry.path, 'rb') as f_in:
                        with zip_obj.open(f'{dir_name}/{entry.name}',
                                          'w') as f_out:
                            f_out.write(f_in.read())

        problem_zip = f'{problem.id}.zip'
        cwd = os.path.abspath(os.path.dirname(__file__))

        with zipfile.ZipFile(problem_zip, 'w') as zip_obj:
            add_description()
            add_IO()
            add_limits()

            processed = ['description', 'input', 'output', 'limits']
            with os.scandir(os.path.join(cwd, 'templates', 'zip')) as it:
                for entry in it:
                    if entry.is_dir() and entry.name not in processed:
                        add_template(entry.path)
