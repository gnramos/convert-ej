from utils import EJudge

import os


class CodeRunner(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())

    def read(self, file):
        """Read the data from the given file.

        Returns a CompetitiveProgrammingProblem.
        """
        raise NotImplementedError

    def write(self, file=None):
        """Write the data into the given file."""
        assert self.problem

        if file:
            assert not os.path.isfile(file)

        raise NotImplementedError
