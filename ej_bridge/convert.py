#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
import inspect
import os
import problem
import readers
import writers


options = {'readers': {m[0]: m[1]
                       for m in inspect.getmembers(readers, inspect.isclass)
                       if issubclass(m[1], problem.Reader)},
           'writers': {m[0]: m[1]
                       for m in inspect.getmembers(writers, inspect.isclass)
                       if issubclass(m[1], problem.Writer)}}


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

    # Update parser.
    parser.description = f'Convert from {args.reader} to {args.writer} ' \
                         'e-judge formats.'
    parser._actions[0].choices = [args.reader]
    parser._actions[0].help = f'Convert from {args.reader} format.'
    parser._actions[1].choices = [args.writer]
    parser._actions[1].help = f'Convert to {args.writer} format.'

    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    reader = getattr(readers, args.reader)(parser)
    writer = getattr(writers, args.writer)(parser)

    # 2nd parsing.
    args = parser.parse_args()

    for file in args.files:
        try:
            print(f'Processing "{file}".')
            problem = reader.read(file, args)
            writer.write(problem, args)
        except ValueError as e:
            print(f'\tError: {e}.')
            print(f'\tFAILED to process "{file}".\n')
