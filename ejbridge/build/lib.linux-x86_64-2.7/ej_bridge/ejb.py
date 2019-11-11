import argparse
from .translation_functions import dir_cf_to_cr


def main():

    parser = argparse.ArgumentParser(description="EJBridge")

    parser.add_argument("-cftocr", "--forcestorunner",
                        type=str, nargs=1, default=None,
                        help="Directory name with all the questions zip\
                              files, to translate a codeforces question to the\
                              coderunner format")

    parser.add_argument("-p", "--penalty", type=str,
                        nargs=1, default=['0, 0, 10, 20, ...'],
                        help="Error penalty argument")

    parser.add_argument("-an", "--allornothing", type=str,
                        nargs=1, default=['1'], help="All or nothing argument")

    parser.add_argument("-sl", "--specificlanguage", type=str,
                        nargs=1, default=[None], help="Argument for creating \
                        only questions that have a specific language")

    args = parser.parse_args()

    if args.forcestorunner:
        if(args.forcestorunner[0].endswith('/')):
            args.forcestorunner[0] = args.forcestorunner[0][:-1]
        dir_cf_to_cr(args.forcestorunner[0], args.penalty[0],
                     args.allornothing[0], args.specificlanguage[0])


if __name__ == "__main__":
    main()
