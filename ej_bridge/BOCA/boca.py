#  -*- coding: utf-8 -*-

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
        raise NotImplementedError

    def add_origin_parser(self, parser):
        """Adds a parser for creating an EJudgeProblem from a file formatted
        for a BOCA EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        raise NotImplementedError

    def read(self, file, args, language='english'):
        """Reads a problem from file and returns it as an EJudgeProblem.

        Keyword arguments:
        file -- the file containing the data for the problem
        args -- the arguments for configuring the EJudgeProblem
        language -- the language the statement of the problem is written in.
        """
        raise NotImplementedError

    def write(self, problem, args):
        """Writes the given EJudgeProblem into a BOCA file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the arguments for configuring the created file
        """
        raise NotImplementedError
