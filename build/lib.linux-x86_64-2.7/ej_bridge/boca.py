from .utils import EJudge, ProblemText, CompetitiveProgrammingProblem as Cpp

import os
import shutil


class Boca(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __init__(self, file=None):
        self.img_path = 'images_boca'
        super().__init__(file)

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

    def write(self, file=None):
        """Write the given data into a file."""
        raise NotImplementedError
