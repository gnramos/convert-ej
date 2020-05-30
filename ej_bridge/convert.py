#!/usr/bin/env python3


from abc import ABC, abstractmethod
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
import inspect
import os
import sys
import readers
import writers


class Parsing(ABC):
    def __init__(self, parser):
        self.add_arguments(parser)

    @abstractmethod
    def add_arguments(parser):
        pass


class DefaultHelpParser(ArgumentParser):
    """Shows "help" in case of an error parsing."""
    def error(self, message):
        self.print_help()
        e_msg = f'error: {message}'
        print('-' * len(e_msg))
        print(e_msg)
        sys.exit(2)


###############################################################################
class BOCAReader(Parsing, readers.BOCA):
    def add_arguments(self, parser):
        """Adds command line arguments for reading a problem in BOCA format."""
        pass

    def read(self, file, args):
        """Reads the problem in the BOCA format."""
        return super().read(file)


class BOCAWriter(Parsing, writers.BOCA):
    def add_arguments(self, parser):
        """Adds command line arguments for writing a problem in BOCA format."""
        parser.add_argument('--tmp', default='/tmp', dest='tmp_dir',
                            help='Directory for storing temporary files')
        parser.add_argument('--notes', action='store_true',
                            help='Include the notes in the PDF')
        parser.add_argument('--tutorial', action='store_true',
                            help='Include the tutorial in the PDF')

    def write(self, ejproblem, args):
        """Writes the problem in the BOCA format."""
        super().write(ejproblem,
                      output_dir=args.output_dir,
                      tmp_dir=args.tmp_dir,
                      add_notes=args.notes,
                      add_tutorial=args.tutorial)


###############################################################################
class CodeRunnerWriter(Parsing, writers.CodeRunner):
    def __init__(self, parser):
        Parsing.__init__(self, parser)
        writers.CodeRunner.__init__(self)

    def add_arguments(self, parser):
        """Adds command line arguments for writing a problem in CodeRunner format."""
        def check_penalty(penalty):
            """Checks the penalty value."""
            ipenalty = int(penalty)
            if ipenalty < 0:
                raise ArgumentTypeError(f'Penalty "{penalty}" cannot be negative')
            return ipenalty

        parser.add_argument('-p', '--penalty',
                            type=check_penalty,
                            default=2,
                            help='Number of attempts without penalty'
                            ' (default 2)')

        parser.add_argument('-aon', '--all-or-nothing',
                            action='store_true',
                            dest='all_or_nothing',
                            help='Set all-or-nothing marking behavior')

        languages = sorted(list(writers.CodeRunner.FILES['source'].keys()))
        parser.add_argument('-al', '--answer-language',
                            dest='answer_language',
                            choices=languages,
                            default='all',
                            help='Set programming language for answer(s)')

    def write(self, ejproblem, args):
        """Writes the problem in the CodeRunner format."""
        super().write(ejproblem,
                      output_dir=args.output_dir,
                      src_lang=args.answer_language,
                      all_or_nothing=args.all_or_nothing,
                      penalty_after=args.penalty)


###############################################################################
class PolygonReader(Parsing, readers.Polygon):
    def add_arguments(self, parser):
        """Adds command line arguments for reading a problem in Polygon format."""
        parser.add_argument('-sl', '--statement-language',
                            dest='stmt_lang',
                            default='english',
                            help='Set statement language')

    def read(self, file, args):
        """Reads the problem in the Polygon format."""
        return super().read(file, args.stmt_lang)


###############################################################################
def base_parser():
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
                files = set(entry.path
                            for entry in it
                            if (entry.is_file() and
                                not entry.name.startswith('.')))
        else:
            raise ArgumentTypeError('Must provide a valid file or directory')
        return files

    def check_dir(path):
        """Check if the given path is of a directory."""
        if os.path.isdir(path):
            return path
        raise ArgumentTypeError(f'{path} is not a directory')

    def list_formats(module):
        return sorted([m[0]
                       for m in inspect.getmembers(getattr(cur_module, module),
                                                   inspect.isclass)
                       if not inspect.isabstract(m[1])])

    cur_module = sys.modules[__name__]

    # If required, the standard "help" action is processed in the 1st parsing
    # step and then the program exits (as per argparse design), thus it would
    # NOT show the e-judge-specific information that is added in runtime.
    # Therefore, help is added only for the second parsing.
    parser = DefaultHelpParser(description='Convert between e-judge formats',
                               add_help=False,
                               formatter_class=RawTextHelpFormatter)

    parser.add_argument('reader', choices=list_formats('readers'),
                        help='Input e-judge format')
    parser.add_argument('writer', choices=list_formats('writers'),
                        help='Output e-judge format')
    parser.add_argument('files', type=list_input,
                        help='Path of a file or a folder of files to convert'
                        ' from reader to writer formats')
    parser.add_argument('-o', '--output_dir', type=check_dir, default='./',
                        help='Path of folder to save converted file(s) into')

    return parser


def get_instances(parser, args):
    """Adds parser arguments and returns reader/writer methods."""
    current_module = sys.modules[__name__]
    reader = getattr(current_module, f'{args.reader}Reader')
    writer = getattr(current_module, f'{args.writer}Writer')

    return reader(parser), writer(parser)


def main():
    # Parsing arguments are added dynamically according to command line
    # arguments, so there are 2 parsing steps.

    # Add command line arguments for specifying reader/writer and source
    # file(s).
    parser = base_parser()
    args, unknown = parser.parse_known_args()

    if args.reader == args.writer:
        exit(0)

    # Get instances for specific reading/writing, which update the parser.
    reader, writer = get_instances(parser, args)

    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    args = parser.parse_args()

    # Process file(s).
    for file in args.files:
        try:
            print(f'Processing "{file}".')
            ejproblem = reader.read(file, args)
            writer.write(ejproblem, args)
        except ValueError as e:
            print(f'\tError: {e}.')
            print(f'\tFAILED to process "{file}".\n')


if __name__ == "__main__":
    main()
