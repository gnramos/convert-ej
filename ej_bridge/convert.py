#!/usr/bin/env python3

import argparse
from importlib import import_module
import os
import sys


class HelpOnErrorParser(argparse.ArgumentParser):
    """Prints help when a parsing error occurs."""
    def error(self, message):
        sys.stderr.write(f'Error: {message}\n\n')
        self.print_help()
        sys.exit(2)


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

    if not files:
        raise ValueError('Must provide a valid file or path.')
    return files


def check_ejudge(ejudge):
    """Checks if the given name is a valid directory."""
    if not os.path.isdir(ejudge):
        raise ValueError(f'No {ejudge} directory found for E-judge files.')
    return ejudge


if __name__ == "__main__":
    # Parsing is done in 3 steps:
    # 1) parse to get the origin/dest e-judge formats and the problem file(s),
    # 2) improve parser according to origin/dest converters' requirements, and
    # 3) parse all arguments.
    #
    # Since adding "help" to the parser handles only the arguments of step 1
    # and exits the program (as per argparse design), it is not useful for
    # helping configuring the converters in step 3. Thus, an intermediate
    # "help hack" is applied to help users with step 1.

    # Step 1 - get origin/dest (and files).
    p = HelpOnErrorParser('Convert between e-judge formats.', add_help=False)

    p.add_argument('origin', type=check_ejudge,
                   help='Path for judge files for origin format.')
    p.add_argument('dest', type=check_ejudge,
                   help='Path for judge files for destination format.')
    p.add_argument('-f', '--files', type=check_files, required=True,
                   help='Path of a file or a folder of files to convert from'
                        ' origin to destination formats.')

    # First parsing step.
    args, unknown = p.parse_known_args()
    if args.origin == args.dest:
        p.exit()

    # Help Hack: show if only origin, dest, and files are given (and help *is*
    # wanted).
    if len(sys.argv) == 6:
        if '-h' in unknown or '--help' in unknown:
            p.print_help()

    # Get classes from origin/dest modules.
    mod_origin = import_module(args.origin + '.' + args.origin.lower())
    mod_dest = import_module(args.dest + '.' + args.dest.lower())

    origin = getattr(mod_origin, args.origin)()
    dest = getattr(mod_dest, args.dest)()

    # Step 2 - improve parser.
    p.description = f'Convert from {args.origin} to {args.dest} ' \
                    'e-judge formats.'
    p.add_argument('-h', '--help', action='help',
                   help='show this help message and exit')
    origin.add_origin_parser(p)
    dest.add_dest_parser(p)

    # Step 3 - get all arguments.
    args = p.parse_args()

    # Do the work.
    for file in args.files:
        try:
            problem = origin.read(file, args)
            dest.write(problem, args)
            print(f'Processed file {file}')
        except ValueError as e:
            print(f'\nUnable to process file {file}\n{e}\n')
