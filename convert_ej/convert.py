#!/usr/bin/env python3


from abc import ABC, abstractmethod
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
import inspect
import os
import sys

try:
    import readers
except:
    from . import readers
try:
    import writers
except:
    from . import writers


class EJudgeParser(ArgumentParser):
    """Provides a custom parser for E-Judges.

    Dynamically adds parsing arguments according to reader/writer as specified
    in command line options.

    Shows the "help" message in case of an error, exits program if reader is
    the same as writer.
    """
    def __init__(self):
        """Constructor."""
        super().__init__(description='Convert between e-judge formats',
                         add_help=False,
                         formatter_class=RawTextHelpFormatter)

        self.add_argument('reader', choices=self._list_formats('readers'),
                          help='Input e-judge format')
        self.add_argument('writer', choices=self._list_formats('writers'),
                          help='Output e-judge format')
        self.add_argument('files', type=self._list_input,
                          help='Path of a file or folder of files to convert'
                          ' from reader to writer formats')
        self.add_argument('-o', '--output_dir', type=self._check_dir,
                          default='./',
                          help='Path of folder to save converted file(s)')

        # Anything different than basic arguments is considered an error and
        # triggers the "help" message.
        args, unknown = super().parse_known_args()

        if args.reader == args.writer:
            exit(0)

        # Add specific arguments.
        curr_module = sys.modules[__name__]
        reader_class = getattr(curr_module, f'{args.reader}Reader')
        writer_class = getattr(curr_module, f'{args.writer}Writer')

        self.reader = reader_class(self)
        self.writer = writer_class(self)

        # All arguments set, add "help" option.
        self.add_argument('-h', '--help', action='help',
                          help='show this help message and exit')

    def _list_input(self, path):
        """Returns a list of the input files.

        Returns all the files inside path, in case it's a directory,
        otherwise returns the single file path.
        """
        files = set()
        if os.path.isfile(path):
            files.add(path)
        elif os.path.isdir(path):
            with os.scandir(path) as it:
                files = set(entry.path for entry in it
                            if (entry.is_file() and
                                not entry.name.startswith('.')))
        else:
            raise ArgumentTypeError('Must provide a valid file/directory')
        return files

    def _check_dir(self, path):
        """Check if the given path is of a directory."""
        if os.path.isdir(path):
            return path
        raise ArgumentTypeError(f'{path} is not a directory')

    def _list_formats(self, module):
        """Return a list of names of classes that can be instantiated from the
        given module."""
        curr = sys.modules[__name__]
        return sorted([m[0]
                       for m in inspect.getmembers(getattr(curr, module),
                                                   inspect.isclass)
                       if not inspect.isabstract(m[1]) and m[0] != 'ABC'])

    def error(self, message):
        """Show "help" on error, if given as argument."""
        if any(help_arg in sys.argv for help_arg in ('-h', '--help')):
            self.print_help()
            sys.exit(0)

        super().error(message)

    def parse_args(self, args=None, namespace=None):
        """Overrides parse_args to add class instances to args."""
        args = super().parse_args(args, namespace)
        args.reader = self.reader
        args.writer = self.writer
        return args

    def parse_known_args(self, args=None, namespace=None):
        """Overrides parse_known_args to add class instances to args."""
        args, unknown = super().parse_known_args(args, namespace)
        args.reader = self.reader
        args.writer = self.writer
        return args, unknown


class Parsing(ABC):
    """Adds arguments for command line parsing."""
    def __init__(self, parser):
        """Creates the instance and adds arguments to the given parser."""
        self.add_arguments(parser)

    @abstractmethod
    def add_arguments(parser):
        """Adds arguments for command line parsing to the given parser."""
        pass


###############################################################################
class BOCAReader(Parsing, readers.BOCA):
    """Interfaces command line parsing with a BOCA reader."""
    def add_arguments(self, parser):
        """Adds command line arguments for reading a problem in BOCA format."""
        pass

    def read(self, file, args):
        """Reads the problem in the BOCA format."""
        return super().read(file)


class BOCAWriter(Parsing, writers.BOCA):
    """Interfaces command line parsing with a BOCA writer."""
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
    """Interfaces command line parsing with a CodeRunnerWriter writer."""
    def __init__(self, parser):
        """Constructor."""
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
    """Interfaces command line parsing with a PolygonReader reader."""
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
def main():
    parser = EJudgeParser()
    args = parser.parse_args()

    for file in args.files:
        try:
            print(f'Processing "{file}".')
            ejproblem = args.reader.read(file, args)
            args.writer.write(ejproblem, args)
        except ValueError as e:
            print(f'\tError: {e}.')
            print(f'\tFAILED to process "{file}".\n')


if __name__ == "__main__":
    main()
