#!/usr/bin/env python3

import argparse
import os

from codeforces import CodeForces
from coderunner import CodeRunner


def _file_or_path_(path):
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
    cf2cr.add_argument('-l', '--language', choices=['C'], default='C',
                       help='Set programming language.')

    return parser


if __name__ == '__main__':
    parser = _parser_()
    args = parser.parse_args()

    if args.command == 'cf2cr':
        for file in args.files:
            if file.endswith('.zip'):
                cf = CodeForces(file)
                cr = CodeRunner()
                cr.problem = cf.problem
                cr.penalty = args.penalty
                cr.all_or_nothing = args.all_or_nothing
                cr.language = args.language

                cr.write()
