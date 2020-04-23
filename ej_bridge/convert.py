#!/usr/bin/env python3

from argparse import ArgumentParser
from importlib import import_module
import os


def check_files(path):
    """Return all the files inside path, in case it's a directory,
    otherwise if it's just a single file, return the file."""
    files = set()
    if os.path.isfile(path):
        files.add(path)
    elif os.path.isdir(path):
        with os.scandir(path) as it:
            files = set(entry.path for entry in it
                        if entry.is_file() and not entry.name.startswith('.'))
    else:
        raise ValueError('Must provide a valid file or path.')
    return files


def check_ejudge(ejudge):
    """Checks if the given name is a valid directory."""
    if not os.path.isdir(ejudge):
        raise ValueError(f'No {ejudge} directory found for E-judge files.')
    return ejudge


if __name__ == "__main__":
    # Parsing arguments are added dynamically according to command line
    # arguments, so there are 2 parsing steps. The first is for "initial"
    # arguments, which define the e-judge formats and the problem files to be
    # processed. With this, the parser is updated to include e-judge-specific
    # arguments, which are then parsed (and the "inital" are parsed again).
    #
    # However, the standard "help" action will be processed in the 1st parsing
    # and then exits the program (as per argparse design), thus it will NOT
    # show the e-judge-specific information.
    #
    # To bypass this, "help" action is only added for the 2nd parsing.

    with os.scandir() as it:
        options = [entry.name
                   for entry in it
                   if entry.is_dir() and not entry.name.startswith(('.', '_'))]

    parser = ArgumentParser(description='Convert between e-judge formats.',
                            add_help=False)

    parser.add_argument('origin', choices=sorted(options),
                        help='Path for judge files for origin format.')
    parser.add_argument('dest', choices=sorted(options),
                        help='Path for judge files for destination format.')
    parser.add_argument('-f', '--files', type=check_files, required=True,
                        help='Path of a file or a folder of files to convert from'
                        ' origin to destination formats.')

    # 1st parsing.
    args, unknown = parser.parse_known_args()
    if args.origin == args.dest:
        exit(0)

    # Get classes from origin/dest modules.
    mod_origin = import_module(args.origin + '.' + args.origin.lower())
    mod_dest = import_module(args.dest + '.' + args.dest.lower())

    origin = getattr(mod_origin, args.origin)()
    dest = getattr(mod_dest, args.dest)()

    # Update parser.
    parser.description = f'Convert from {args.origin} to {args.dest} ' \
                         'e-judge formats.'
    parser._actions[0].choices = [args.origin]
    parser._actions[0].help = f'Convert from {args.origin} format.'
    parser._actions[1].choices = [args.dest]
    parser._actions[1].help = f'Convert to {args.dest} format.'

    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    origin.add_origin_parser(parser)
    dest.add_dest_parser(parser)

    # 2nd parsing.
    args = parser.parse_args()

    for file in args.files:
        try:
            problem = origin.read(file, args)
            dest.write(problem, args)
            print(f'Processed file {file}')
        except ValueError as e:
            print(f'\nUnable to process file {file}\n{e}\n')
