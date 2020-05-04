#  -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Statement():
    """Stores the information required to state a problem.

    Keep in mind that:
      - text is formatted for TeX processing;
      - images are stored as {file_name: binobj} entries in a dict where binobj
      is a bytes-like object.
    """

    def __init__(self, title, description, in_format, out_format, examples,
                 images={}, tags=[], tutorial=None, notes=None):
        """Class constructor.

        Keyword arguments:
        title -- short sentence describing the problem
        description -- problem specification
        in_format -- description of input format
        out_format -- description of output format
        examples -- list of dict entries with 'in' (input) files and the
                    expected 'out' (output) result
        images -- dict of images used in the description (default {})
        tags -- list of tags for indexing the problem (default [])
        tutorial -- instructions on how to solve the problem (default None)
        notes -- comments on the problem (notes, emphasis on a specific detail
                 or example, etc.) (default None)
        """

        self.title = title
        self.description = description
        self.input = in_format
        self.output = out_format
        self.examples = examples
        self.images = images
        self.tags = tags
        self.tutorial = tutorial
        self.notes = notes

        assert title
        assert description
        assert in_format
        assert out_format
        assert examples
        for ex in examples:
            assert 'in' in ex
            assert ex['in']
            assert 'out' in ex
            assert ex['out']
        if images:
            assert isinstance(images, dict)


class Evaluation():
    """Stores the information required to evaluate a problem."""

    def __init__(self, tests, solutions, limits):
        """Class constructor.

        Keyword arguments:
        tests -- dict of 'examples' and 'hidden' test cases, each case has a
                      dict of 'in' (input) data and its expected 'out'
                      (output).
        solutions -- list of solutions dicts, in the preferred order, where
                     each entry is {file_extension: source_code}.
        limits -- dict of 'time_sec' and 'memory_MB' limits for evaluation a
                  solution.
        """
        self.tests = tests
        self.solutions = solutions
        self.limits = limits

        assert tests['examples'] or tests['hidden']
        assert solutions
        assert solutions[0] and isinstance(solutions[0], dict)
        assert limits['time_sec'] > 0
        assert limits['memory_MB'] > 0


class EJudgeProblem():
    """Stores the information required to present and evaluate a problem."""

    def __init__(self, id, statement, evaluation):
        """Class constructor.

        Keyword arguments:
        id -- a unique identifier (handle) for this problem, useful for
              database indexing.
        statement -- an instance of Statement that describes the problem.
        evaluation -- an instance of Evaluation for evaluating a problem.
        """
        self.id = id
        self.statement = statement
        self.evaluation = evaluation

        assert id
        assert isinstance(statement, Statement)
        assert isinstance(evaluation, Evaluation)


class Reader(ABC):
    """Base class for reading from an EJudge file."""

    @abstractmethod
    def read(self, file):
        """Reads a problem from file and returns it as an EJudgeProblem.

        Keyword arguments:
        file -- the file containing the data for the problem
        """
        raise NotImplementedError


class Writer(ABC):
    """Base class for reading to an e-judge file."""

    @abstractmethod
    def write(self, problem, output_dir='./'):
        """Writes the given EJudgeProblem into a file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        output_dir -- the directory to write the file created
        """
        raise NotImplementedError
