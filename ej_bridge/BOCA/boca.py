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
        pass

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
        language -- the language the statement of the problem is written in.
        """
        raise NotImplementedError

    def write(self, problem, args, tmp_dir='/tmp'):
        """Writes the given EJudgeProblem into a BOCA file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the arguments for configuring the created file
        """

        def copy_template_files(dir_name):
            with os.scandir(os.path.join(cwd, f'template/{dir_name}')) as it:
                for entry in it:
                    with open(entry.path, 'rb') as f:
                        content = f.read()
                    with zip_obj.open(f'{dir_name}/{entry.name}', 'w') as f:
                        f.write(content)

        def add_description():
            def add_pdf():
                def image_files():
                    for name, img in problem.statement.images.items():
                        with open(os.path.join(tmp_dir, name), 'wb') as f:
                            f.write(img)

                def make_tex():
                    def rows(examples):
                        def cell(ex):
                            verbatim = f'\\begin{{verbatim}}\n{ex}\\end{{verbatim}}'
                            return f'\\vspace{{-1.2\\baselineskip}}%\n{verbatim}\n\\vspace*{{-2\\baselineskip}}%'
                        return ''.join('{}\n&\n{}\n\\\\\hline'.format(cell(ex['in']), cell(ex['out']))
                                       for ex in examples)

                    with open(os.path.join(cwd, 'template.tex')) as f:
                        tex = f.read()

                    stmt = problem.statement
                    tex = tex.replace('[[TITLE]]', stmt.title)
                    tex = tex.replace('[[DESCRIPTION]]', stmt.description)
                    tex = tex.replace('[[INPUT]]', stmt.input)
                    tex = tex.replace('[[OUTPUT]]', stmt.output)
                    tex = tex.replace('[[VERBATIM_EXAMPLE_ROWS]]', rows(stmt.examples))
                    if stmt.notes:
                        tex = tex.replace('[[NOTES]]', stmt.notes)
                    else:
                        tex = tex.replace(r'\textbf{Notes}', '')
                        tex = tex.replace('[[NOTES]]', '')

                    with open(tex_file, 'w') as f:
                        f.write(tex)

                def pdflatex():
                    env = os.environ.copy()
                    env['TEXINPUTS'] = f'.:{tmp_dir}//:'
                    cmd = ['pdflatex', '-output-directory=' + tmp_dir,
                           '-interaction=nonstopmode', '-halt-on-error', tex_file]
                    with open(os.devnull, 'w') as DEVNULL:
                        try:
                            subprocess.check_call(cmd, env=env, stdout=DEVNULL)
                        except:
                            try:
                                # run again to show errors
                                subprocess.check_call(cmd, env=env)
                            except Exception as e:
                                raise ValueError(f'Unable to create pdf from {tex_file}.')

                tex_file = os.path.join(tmp_dir, f'{problem.id}.tex')
                make_tex()
                image_files()
                pdflatex()

                pdf_file = tex_file.replace('tex', 'pdf')
                with open(pdf_file, 'rb') as f:
                    pdf = f.read()

                pdf_file = os.path.split(pdf_file)[-1]
                zip_obj.writestr(f'description/{pdf_file}', pdf)

                return pdf_file

            def add_problem_info():
                zip_obj.writestr('description/problem.info',
                                 f'basename={problem.id}\n'
                                 f'fullname={problem.statement.title}\n'
                                 f'descfile={pdf_file}\n')

            pdf_file = add_pdf()
            add_problem_info()

        def add_IO():
            for key, tests in problem.evaluation.test_cases.items():
                for name, files in tests.items():
                    for k, data in files.items():
                        zip_obj.writestr(f'{k}put/{name}', data)

        def add_limits():
            with os.scandir(os.path.join(cwd, f'template/limits')) as it:
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

        problem_zip = f'{problem.id}.zip'
        cwd = os.path.abspath(os.path.dirname(__file__))

        with zipfile.ZipFile(problem_zip, 'w') as zip_obj:
            copy_template_files('compare')
            copy_template_files('compile')
            add_description()
            add_IO()
            add_limits()
            copy_template_files('run')
            # copy_template_files('tests')
