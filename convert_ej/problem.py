#  -*- coding: utf-8 -*-


class Statement():
    """Stores the information required to state a problem.

    Keep in mind that:
      - text is formatted for TeX processing;
      - images are stored as {file_name: binobj} entries in a dict where binobj
      is a bytes-like object.
    """

    def __init__(self, title, description, in_format, out_format, examples,
                 aux_files={}, tags=[], tutorial=None, notes=None):
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
        self.aux_files = aux_files
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
        if aux_files:
            assert isinstance(aux_files, dict)


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
        assert limits['maxfilesize_KB'] > 0


class Problem():
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
