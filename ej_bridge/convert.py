#!/usr/bin/env python3


from argparse import ArgumentParser, RawTextHelpFormatter
import inspect
import os
import readers
import sys
import writers


class DefaultHelpParser(ArgumentParser):
    """Shows "help" in case of an error parsing."""
    def error(self, message):
        self.print_help()
        e_msg = f'error: {message}'
        print('-' * len(e_msg))
        print(e_msg)
        sys.exit(2)


###############################################################################
def boca_reader_add_arguments(parser):
    """Adds command line arguments for reading a problem in BOCA format."""
    pass


def boca_read(file, args):
    """Reads the problem in the BOCA format."""
    return readers.boca(file)


def boca_writer_add_arguments(parser):
    """Adds command line arguments for writing a problem in BOCA format."""
    parser.add_argument('--tmp', default='/tmp', dest='tmp_dir',
                        help='Directory for storing temporary files')
    parser.add_argument('-b', '--basename', default=None,
                        help='Basename for problem description')
    parser.add_argument('--notes', action='store_true',
                        help='Include the notes in the PDF')
    parser.add_argument('--tutorial', action='store_true',
                        help='Include the tutorial in the PDF')


def boca_write(ejproblem, args):
    """Writes the problem in the BOCA format."""
    writers.boca(ejproblem,
                 output_dir=args.output_dir,
                 tmp_dir=args.tmp_dir,
                 basename=args.basename,
                 add_notes=args.notes,
                 add_tutorial=args.tutorial)


###############################################################################
def coderunner_writer_add_arguments(parser):
    """Adds command line arguments for writing a problem in CodeRunner format."""
    def check_penalty(penalty):
        """Checks the penalty value."""
        if penalty < 0:
            raise ValueError('Penalty {penalty} cannot be negative')

        return penalty

    parser.add_argument('-p', '--penalty',
                        type=check_penalty,
                        default=2,
                        help='Number of attempts without penalty'
                        ' (default 2)')

    parser.add_argument('-aon', '--all-or-nothing',
                        action='store_true',
                        dest='all_or_nothing',
                        help='Set all-or-nothing marking behavior')

    languages = sorted(list(writers.CODERUNNER['types'].keys()))
    parser.add_argument('-al', '--answer-language',
                        dest='answer_language',
                        choices=languages,
                        default='all',
                        help='Set programming language for answer(s)')


def coderunner_write(ejproblem, args):
    """Writes the problem in the CodeRunner format."""
    writers.coderunner(ejproblem,
                       output_dir=args.output_dir,
                       src_lang=args.answer_language,
                       all_or_nothing=args.all_or_nothing,
                       penalty_after=args.penalty)


###############################################################################
def polygon_reader_add_arguments(parser):
    """Adds command line arguments for reading a problem in Polygon format."""
    parser.add_argument('-sl', '--statement-language',
                        dest='stmt_lang',
                        default='english',
                        help='Set statement language')


def polygon_read(file, args):
    """Reads the problem in the Polygon format."""
    return readers.polygon(file, args.stmt_lang)


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
                files = set(entry.path
                            for entry in it
                            if (entry.is_file() and
                                not entry.name.startswith('.')))
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
                       for m in inspect.getmembers(readers,
                                                   inspect.isfunction)])

    def list_writers():
        return sorted([m[0]
                       for m in inspect.getmembers(writers,
                                                   inspect.isfunction)])

    # If required, the standard "help" action is processed in the 1st parsing
    # step and then the program exits (as per argparse design), thus it would
    # NOT show the e-judge-specific information that is added in runtime.
    # Therefore, help is added only for the second parsing.
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

    args, unknown = parser.parse_known_args()
    return parser, args


def second_parsing(parser, args):
    """Adds parser arguments for reader/writer methods."""
    current_module = sys.modules[__name__]

    add_reader = getattr(current_module, f'{args.reader}_reader_add_arguments')
    add_writer = getattr(current_module, f'{args.writer}_writer_add_arguments')

    add_reader(parser)
    add_writer(parser)

    # Add help for parsing all arguments, if required.
    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    return parser, parser.parse_args()


def get_methods(reader, writer):
    """Adds parser arguments and returns reader/writer methods."""
    current_module = sys.modules[__name__]
    reader = getattr(current_module, f'{reader}_read')
    writer = getattr(current_module, f'{writer}_write')

    return reader, writer


if __name__ == "__main__":
    # Parsing arguments are added dynamically according to command line
    # arguments, so there are 2 parsing steps.

    # Add command line arguments for specifying reader/writer and source
    # file(s).
    parser, args = first_parsing()

    if args.reader == args.writer:
        exit(0)

    # Add command line arguments for specific reader/writer.
    parser, args = second_parsing(parser, args)

    # Get methods for specific reading/writing.
    reader, writer = get_methods(args.reader, args.writer)

    # Process file(s).
    args = parser.parse_args()
    for file in args.files:
        try:
            print(f'Processing "{file}".')
            ejproblem = reader(file, args)
            writer(ejproblem, args)
        except ValueError as e:
            print(f'\tError: {e}.')
            print(f'\tFAILED to process "{file}".\n')
