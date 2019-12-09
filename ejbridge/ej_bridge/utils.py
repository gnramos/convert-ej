from abc import ABC, abstractmethod

import re
import os


class ProblemText():
    """Stores the textual information for a problem."""

    def __init__(self, name, context, input, output, tutorial=None,
                 images=[], notes=None):
        """Constructor."""
        self.name = name
        self.context = context
        self.input = input
        self.output = output
        self.images = images
        self.tutorial = tutorial
        self.notes = notes

        if self.name is None or len(self.name) == 0:
            raise NameError('Name not found')
        if self.context is None or len(self.context) == 0:
            raise NameError('Legend not found')
        if self.input is None or len(self.input) == 0:
            raise NameError('Input text not found')
        if self.output is None or len(self.output) == 0:
            raise NameError('Output text not found')

        if self.images:
            for img in self.images:
                assert os.path.isfile(os.path.join('images', img))


class CompetitiveProgrammingProblem():
    """Stores the data for a competitive programming problem."""

    def __init__(self, handle, text, test_cases, solutions, sol_type,
                 tags, memory_limit, time_limit):
        """Constructor."""
        self.handle = handle
        self.text = text
        self.test_cases = test_cases
        self.solutions = solutions
        self.sol_type = sol_type
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
        assert self.sol_type is not None
        assert len(self.sol_type) > 0
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


def tex2html(s):
    """
    Return a string with syntax substitutions,
    from LaTeX format to html, performed on the
    given input.
    Arguments:
    s -- input string to be formated
    """

    # Convert the mathematical equations
    s = re.sub(r'\$([^\$]*)\$', r'\\( \1 \\)', s)
    s = re.sub(r'\$\$([^\$]*)\$\$', r'<p><br />\\( \1 \\)<br /></p>', s)

    # Image
    s = re.sub(r'.eps', r'.png', s)
    s = re.sub(r'\\includegraphics\[([^\]]*)\]\{([^\}]*)\}',
               r'<img src="@@PLUGINFILE@@/\2"><br>', s)

    # Dict with all the substitution rules for a specific format
    rules1 = {
        r'\\begin{itemize}': '<ul>',
        r'\\end{itemize}': '</ul>',
        r'\\begin{center}': '<p style="text-align: center;">',
        r'\\end{center}': '</p>',
        r'\`\`': '\"',
        r'\'\'': '\"',
        r'\\arrowvert': '|',
        r'\\\^': '^',
        r'\n\n': '</p>\n\n<p>\n'
    }
    rules2 = {
        r'\\emph': 'i',
        r'\\textbf': 'b',
        r'\\textit': 'i'
        # r'\\textsc': '',
        # r'\\texttt': '',
        # r'\\textsf': '',
        # r'\\textrm': '',
        # r'\\textsl': ''
    }
    rules3 = {
        r'\\item': 'li'
    }

    # Apply the rules to the string
    for l, h in rules1.items():
        s = re.sub(l, h, s)

    for l, h in rules2.items():
        l_str = r'%s{([^}]*)}' % l
        h_str = r'<%s>\1</%s>' % (h, h)
        s = re.sub(l_str, h_str, s)

    for l, h in rules3.items():
        l_str = r'%s([^\n]*)' % l
        h_str = r'<%s>\1</%s>' % (h, h)
        s = re.sub(l_str, h_str, s)

    return s
