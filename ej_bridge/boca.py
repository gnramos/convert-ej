from .utils import EJudge, pdflatex, makenew_dir

import os
import shutil


class Boca(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __init__(self):
        self.img_path = 'images_boca'
        self.contest_dir = 'contest'

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())

    def __del__(self):
        """Delete the image path, if it exists."""
        if os.path.isdir(self.img_path):
            shutil.rmtree(self.img_path)

    def read_data(self, problem):
        """Read the data from the other class, and create a new image path."""
        if problem.text.images:
            shutil.copytree(problem.text.img_path, self.img_path)
            problem.text.img_path = self.img_path
        self.problem = problem

    def read(self, file):
        """Read the data from the given file."""
        raise NotImplementedError

    def write(self):
        """Write the given data into a file."""

        def write_tests(test_cases, question_dir):
            """Write the test cases on the input and output
            directories."""

            x = 1
            for t_in, t_out in zip(test_cases['hidden']['in'],
                                   test_cases['hidden']['out']):
                with open(os.path.join(question_dir, 'input',
                                       str(x)), 'w') as f_in:
                    f_in.write(t_in)
                with open(os.path.join(question_dir, 'output',
                                       str(x)), 'w') as f_out:
                    f_out.write(t_out)
                x = x+1
            for t_in, t_out in zip(test_cases['example']['in'],
                                   test_cases['example']['out']):
                with open(os.path.join(question_dir, 'input',
                                       str(x)), 'w') as f_in:
                    f_in.write(t_in)
                with open(os.path.join(question_dir, 'output',
                                       str(x)), 'w') as f_out:
                    f_out.write(t_out)
                x = x+1

        def write_text(question_dir, text, tags, n_ex, let):
            """Write the text on a LaTeX file, and copy the images to the
            question directory."""

            texto = ''
            texto += '\\NomeDoProblema{' + text.name.rstrip() + '}\n'
            texto += '\\Conceitos{' + ', '.join(tags) + '}\n\n'
            texto += text.context + '\n'
            texto += '\\Entrada\n\n' + text.input + '\n'
            texto += '\\Saida\n\n' + text.output + '\n'
            texto += '\\Exemplos{' + \
                     ', '.join([str(p) for p in range(1, n_ex+1)]) + '}\n\n'
            if text.notes:
                texto += '\\Notas\n\n' + text.notes + '\n'

            with open(os.path.join(question_dir, let+'.tex'), 'w') as texfile:
                texfile.write(texto)

            def cpy_images(question_dir):
                for img in text.images:
                    shutil.copy(os.path.join(text.img_path, img),
                                question_dir)

            cpy_images(question_dir)

        def get_letter(num):
            """Return the num-th uppercase letter."""
            return chr(ord('A')+num)

        if not self.problem:
            raise Exception('Intermediate class not found.')

        letter = 0
        makenew_dir(self.contest_dir)

        # Iterate through the problems later

        package_dir = os.path.abspath(os.path.dirname(__file__))
        template_dir = os.path.join(package_dir, 'Boca_Templates', 'question')
        question_dir = os.path.join(self.contest_dir, get_letter(letter))
        shutil.copytree(template_dir, question_dir)
        write_tests(self.problem.test_cases, question_dir)
        num_examples = len(self.problem.test_cases['example']['in'])
        write_text(question_dir, self.problem.text,
                   self.problem.tags, num_examples, get_letter(letter))
