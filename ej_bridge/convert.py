#!/usr/bin/env python3


from abc import ABC, abstractmethod
from argparse import ArgumentParser, RawTextHelpFormatter
import inspect
import os
from problem import Reader as ProblemReader, Writer as ProblemWriter
import readers
import sys
import writers


class DefaultHelpParser(ArgumentParser):
    def error(self, message):
        self.print_help()
        e_msg = f'error: {message}'
        print('-' * len(e_msg))
        print(e_msg)
        sys.exit(2)


class AddsArguments(ABC):
    """Base class for adding parser arguments."""
    @abstractmethod
    def __init__(self, parser):
        raise NotImplementedError


class BOCAWriter(AddsArguments, writers.BOCA):
    """Parses command line arguments for BOCA e-judge."""
    def __init__(self, parser):
        """Adds arguments for creating a file formatted for BOCA e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        parser.add_argument('--tmp', default='/tmp', dest='tmp_dir',
                            help='Directory for storing temporary files')
        parser.add_argument('-b', '--basename', default=None,
                            help='Basename for problem description')
        parser.add_argument('--notes', action='store_true',
                            help='Include the notes in the PDF')
        parser.add_argument('--tutorial', action='store_true',
                            help='Include the tutorial in the PDF')

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


class CodeRunnerWriter(AddsArguments, writers.CodeRunner):
    """Parses command line arguments for CodeRunner e-judge."""
    def __init__(self, parser):
        """Adds arguments for creating a file formatted for CodeRunner e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        def check_penalty(penalty):
            """Checks the penalty value."""
            if penalty < 0:
                raise ValueError('Penalty {penalty} cannot be negative')

            return penalty

        parser.add_argument('--penalty',
                            type=check_penalty,
                            default=2,
                            help='Number of attempts without penalty'
                            ' (default 2)')

        parser.add_argument('-aon', '--all-or-nothing',
                            action='store_true',
                            dest='all_or_nothing',
                            help='Set all-or-nothing marking behavior')

        languages = sorted(list(writers.CodeRunner.accepted['types'].keys()))
        parser.add_argument('-al', '--answer-language',
                            dest='answer_language',
                            choices=languages,
                            default='all',
                            help='Set programming language for answer(s)')

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


class PolygonReader(AddsArguments, readers.Polygon):
    """Parses command line arguments for a Polygon package from CodeForces
    e-judge.
    """
    def __init__(self, parser):
        """Adds arguments for reading from a file formatted for CodeForces
        e-judge.

        Keyword arguments:
        parser -- the parser to configure
        """
        parser.add_argument('-sl', '--statement-language',
                            dest='stmt_lang',
                            default='english',
                            help='Set statement language')

    def read(self, file, args):
        """Reads a problem from file and returns it as an EJudgeProblem.

        Keyword arguments:
        file -- the file containing the data for the problem
        args -- the parsed command line arguments
        """
        return super().read(file, args.stmt_lang)


###############################################################################
def first_parsing():
    """Creates a parser with default arguments and parses it."""
    def list_input(path):
        """Returns a list of the input files.

        Returns all the files inside path, in case it's a directory, otherwise
        returns the single file path.
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

    def check_dir(path):
        """Check if the given path is of a directory."""
        if os.path.isdir(path):
            return path
        raise ValueError(f'{path} is not a directory')

    def list_readers():
        return sorted([m[0]
                       for m in inspect.getmembers(readers, inspect.isclass)
                       if issubclass(m[1], ProblemReader)])

    def list_writers():
        return sorted([m[0]
                       for m in inspect.getmembers(writers, inspect.isclass)
                       if issubclass(m[1], ProblemWriter)])

    # If required, the standard "help" action is processed in the 1st parsing
    # step and then the program exits (as per argparse design), thus it would
    # NOT show the e-judge-specific information that is added in runtime. Thus,
    # help is not added here.
    parser = DefaultHelpParser(description='Convert between e-judge formats',
                               add_help=False,
                               formatter_class=RawTextHelpFormatter)

    parser.add_argument('reader', choices=list_readers(),
                        help='Input e-judge format')
    parser.add_argument('writer', choices=list_writers(),
                        help='Output e-judge format')
    parser.add_argument('files', type=list_input,
                        help='Path of a file or a folder of files to convert'
                        ' from reader to writer formats')
    parser.add_argument('-o', '--output_dir', type=check_dir, default='./',
                        help='Path of folder to save converted file(s) into')

    # 1st parsing.
    args, unknown = parser.parse_known_args()
    return parser, args


def get_instances(parser):
    """Return reader/writer instances."""
    current_module = sys.modules[__name__]
    reader = getattr(current_module, f'{args.reader}Reader')(parser)
    writer = getattr(current_module, f'{args.writer}Writer')(parser)

    return reader, writer


if __name__ == "__main__":
    # Parsing arguments are added dynamically according to command line
    # arguments, so there are 2 parsing steps.
    parser, args = first_parsing()

    if args.reader == args.writer:
        exit(0)

    # Instances also update the parser with their specific arguments.
    reader, writer = get_instances(parser)

    # Add help for parsing all arguments, if required.
    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

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
