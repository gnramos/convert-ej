#!/usr/bin/env python3

from .codeforces import CodeForces
from .coderunner import CodeRunner

import argparse
import os
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s\n',
    datefmt='%m/%d/%Y - %I:%M:%S %p')


def _file_or_path_(path):
    """Return all the files inside path, in case it's a directory,
    otherwise if it's just a single file, return the file."""
    files = set()
    if os.path.isfile(path):
        files.add(path)
    elif os.path.isdir(path):
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.add(entry.path)
    return files


def _parser_():
    parser = argparse.ArgumentParser(description='Translate competitive \
                                     programming problems between e-judges.')

    subparsers = parser.add_subparsers(dest='command')

    cf2cr = subparsers.add_parser('cf2cr',
                                  description='Translate CodeForces packages \
                                               to CodeRunner XML.',
                                  help='Help on transforming CodeForces \
                                        package(s) into CodeRunner XML(s).')

    cf2cr.add_argument('files', type=_file_or_path_,
                       help='Path of a file or a folder of files.')
    cf2cr.add_argument('-p', '--penalty',
                       choices=['0, 0, 10, 20, ...', '10, 20, ...',
                                '0, 0, ...'],
                       default=['0, 0, 10, 20, ...'], metavar='P',
                       help='Set marking penalty regime. Options are:\
                             \n\"0, 0, 10, 20, ...\" (default), \
                             \n\"0, 0, ...\",\n or \"10, 20, ...\"')
    cf2cr.add_argument('-an', '--allornothing', action='store_true',
                       dest='all_or_nothing',
                       help='Set all-or-nothing marking behavior.')
    cf2cr.add_argument('-l', '--language', choices=['c', 'cpp', 'python'],
                       default='c', help='Set programming language.')

    return parser


def main():
    parser = _parser_()
    args = parser.parse_args()

    if args.command == 'cf2cr':
        for file in args.files:
            if file.endswith('.zip'):
                try:
                    cf = CodeForces(args.language, file)
                    cr = CodeRunner(args.penalty, args.all_or_nothing)
                    cr.read_data(cf.problem)
                    cr.write()
                    del cf
                    del cr
                except Exception as err_list:
                    for error in err_list.args:
                        logging.error('Error: {}'.format(error))
                    logging.error('It was not possible to generate '
                                  'the question \'{}\'.'.format(file[:-4]))
                else:
                    logging.info('Question \'{}\' was successfully generated!'
                                 .format(file[:-4]))
        if not args.files:
            logging.error('Path or file doesn\'t exist.')
    elif args.command == 'cf2boca':
        pass


if __name__ == "__main__":
    main()
