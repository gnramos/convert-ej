#!/usr/bin/env python3


from abc import ABC
from argparse import ArgumentParser, RawTextHelpFormatter
import inspect
import os
import problem
import readers
import sys
import writers


class HasParser(ABC):
    """Base class for parsing command line arguments."""
    def __init__(self, parser):
        self.parser = parser


class BOCAWriter(HasParser, writers.BOCA):
    """Parses command line arguments for BOCA e-judge."""
    def __init__(self, parser):
        """Adds arguments for creating a file formatted for BOCA e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        super().__init__(parser)

        self.parser.add_argument('--tmp', default='/tmp', dest='tmp_dir',
                                 help='Directory for storing temporary files.'
                                 ' (default /tmp)')
        self.parser.add_argument('-b', '--basename', default=None,
                                 help='Basename for problem description.')
        self.parser.add_argument('--notes', action='store_true',
                                 help='Include the notes in the PDF.')
        self.parser.add_argument('--tutorial', action='store_true',
                                 help='Include the tutorial in the PDF.')

    def write(self, problem, args):
        """Writes the given EJudgeProblem into a BOCA file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the parsed command line arguments
        """
        return super().write(problem,
                             output_dir=args.output_dir,
                             tmp_dir=args.tmp_dir,
                             basename=args.basename,
                             add_notes=args.notes,
                             add_tutorial=args.tutorial)


class CodeRunnerWriter(HasParser, writers.CodeRunner):
    """Parses command line arguments for CodeRunner e-judge."""
    def __init__(self, parser):
        """Adds arguments for creating a file formatted for CodeRunner e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        super().__init__(parser)

        self.parser.add_argument('--penalty',
                                 type=self.check_penalty,
                                 default=2,
                                 help='Number of attempts without penalty.'
                                 ' (default 2)')

        self.parser.add_argument('-aon', '--all-or-nothing',
                                 action='store_true',
                                 dest='all_or_nothing',
                                 help='Set all-or-nothing marking behavior.')

        languages = sorted(list(writers.CodeRunner.accepted['types'].keys()))
        self.parser.add_argument('-al', '--answer-language',
                                 dest='answer_language',
                                 choices=languages,
                                 default='all',
                                 help='Set programming language for '
                                      'answer(s).')

    def _check_penalty(penalty):
        """Checks the penalty value."""
        if penalty < 0:
            raise ValueError('Penalty {penalty} cannot be negative')

        return penalty

    def write(self, problem, args):
        """Writes the given EJudgeProblem into a CodeRunner file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the parsed command line arguments
        """
        return super().write(problem,
                             output_dir=args.output_dir,
                             src_lang=args.answer_language,
                             all_or_nothing=args.all_or_nothing,
                             penalty_after=args.penalty)


class PolygonReader(HasParser, readers.Polygon):
    """Parses command line arguments for a Polygon package from CodeForces
    e-judge.
    """
    def __init__(self, parser):
        """Adds arguments for reading from a file formatted for CodeForces
        e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        super().__init__(parser)

        self.parser.add_argument('-sl', '--statement-language',
                                 dest='stmt_lang',
                                 default='english',
                                 help='Set statement language.')

    def read(self, file, args):
        """Reads a problem from file and returns it as an EJudgeProblem.

        Keyword arguments:
        file -- the file containing the data for the problem
        args -- the parsed command line arguments
        """
        return super().read(file, args.stmt_lang)


###############################################################################
def first_parsing():
    def check_input(path):
        """Returns all the files inside path, in case it's a directory, otherwise
        return the single file path.
        """
        files = set()
        if os.path.isfile(path):
            files.add(path)
        elif os.path.isdir(path):
            with os.scandir(path) as it:
                files = set(entry.path for entry in it
                            if entry.is_file() and not entry.name.startswith('.'))
        else:
            raise ValueError('Must provide a valid file or directory')
        return files

    def check_output(path):
        if os.path.isdir(path):
            return path
        raise ValueError(f'{path} is not a directory')

    options = {'readers': {m[0]: m[1]
                           for m in inspect.getmembers(readers, inspect.isclass)
                           if issubclass(m[1], problem.Reader)},
               'writers': {m[0]: m[1]
                           for m in inspect.getmembers(writers, inspect.isclass)
                           if issubclass(m[1], problem.Writer)}}

    parser = ArgumentParser(description='Convert between e-judge formats.',
                            add_help=False,
                            formatter_class=RawTextHelpFormatter)

    parser.add_argument('reader', choices=sorted(list(options[
                                            'readers'].keys())),
                        help='Input e-judge format.')
    parser.add_argument('writer', choices=sorted(list(options[
                                            'writers'].keys())),
                        help='Output e-judge format.')
    parser.add_argument('-f', '--files', type=check_input, required=True,
                        help='Path of a file or a folder of files to convert'
                        ' from reader to writer formats.')
    parser.add_argument('-o', '--output_dir', type=check_output, default='./',
                        help='Path of folder to save converted file(s) into.'
                        ' (default ./)')

    # 1st parsing.
    args, unknown = parser.parse_known_args()
    if args.reader == args.writer:
        exit(0)

    # Update parser
    args, unknown = parser.parse_known_args()

    parser.description = f'Convert from {args.reader} to {args.writer} ' \
                         'e-judge formats.'
    parser._actions[0].choices = [args.reader]
    parser._actions[0].help = f'Convert from {args.reader} format.'
    parser._actions[1].choices = [args.writer]
    parser._actions[1].help = f'Convert to {args.writer} format.'

    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    return parser, args


if __name__ == "__main__":
    # Parsing arguments are added dynamically according to command line
    # arguments, so there are 2 parsing steps. The first is for "initial"
    # arguments, which define the e-judge formats and the problem files to be
    # processed. With this, the parser is updated to include e-judge-specific
    # arguments, which are then parsed (along with the "initial" ones).
    #
    # However, if required, the standard "help" action would be processed in
    # the 1st parsing and then the program would exit (as per argparse design),
    # thus it would NOT show the e-judge-specific information.
    #
    # To bypass this, "help" action is only added for the 2nd parsing.

    parser, args = first_parsing()

    current_module = sys.modules[__name__]
    reader = getattr(current_module, f'{args.reader}Reader')(parser)
    writer = getattr(current_module, f'{args.writer}Writer')(parser)

    # 2nd parsing.
    args = parser.parse_args()

    for file in args.files:
        try:
            print(f'Processing "{file}".')
            ej_problem = reader.read(file, args)
            writer.write(ej_problem, args)
        except ValueError as e:
            print(f'\tError: {e}.')
            print(f'\tFAILED to process "{file}".\n')
