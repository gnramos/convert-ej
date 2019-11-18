from abc import ABC, abstractmethod


class ProblemText():
    """Stores the textual information for a problem."""

    def __init__(self, name, context, input, output, tutorial, notes=None, images=[]):
        """Constructor."""
        self.name = name
        self.context = context
        self.input = input
        self.output = output
        self.tutorial = tutorial
        self.notes = notes
        self.images = images

        assert self.name is not None
        assert len(self.name) > 0
        assert self.context is not None
        assert len(self.context) > 0
        assert self.input is not None
        assert len(self.input) > 0
        assert self.output is not None
        assert len(self.output) > 0
        assert self.tutorial is not None
        assert len(self.tutorial) > 0


class CompetitiveProgrammingProblem():
    """Stores the data for a competitive programming problem."""

    def __init__(self, handle, text, images, test_cases, solutions, tags,
                 memory_limit, time_limit):
        """Constructor."""
        self.handle = handle
        self.text = text
        self.images = images
        self.test_cases = test_cases
        self.solutions = solutions
        self.tags = tags
        self.memory_limit = memory_limit
        self.time_limit = time_limit

        assert self.handle is not None
        assert len(self.handle) > 0
        assert self.text is not None
        # assert len(self.text) > 0
        assert self.test_cases is not None
        assert len(self.test_cases) > 0
        assert self.solutions is not None
        assert len(self.solutions) > 0
        assert self.tags is not None
        assert len(self.tags) > 0
        assert self.memory_limit > 0
        assert self.time_limit > 0

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())


class EJudge(ABC):
    """Manipulates a CompetitiveProgrammingProblem file."""

    def __init__(self, file=None):
        """Constructor."""
        if file:
            self.read(file)
        else:
            self.problem = None

    @abstractmethod
    def read(self, file):
        """Read the data from the given file.

        Stores the data in the "problem" attribute.
        """
        pass

    @abstractmethod
    def write(self, file=None):
        """Write the data into the given file."""
        pass
