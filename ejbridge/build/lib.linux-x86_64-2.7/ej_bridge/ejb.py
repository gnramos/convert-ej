import argparse
from .translation_functions import dir_cf_to_cr


def main():

    parser = argparse.ArgumentParser(description="EJBridge")

    parser.add_argument("-cftocr", "--forcestorunner",
                        type=str, nargs=1, default=None,
                        help="Directory name with all the questions zip\
                              files, to translate a codeforces question to the\
                              coderunner format")

    args = parser.parse_args()

    if args.forcestorunner:
        if(args.forcestorunner[0].endswith('/')):
            args.forcestorunner[0] = args.forcestorunner[0][:-1]
        dir_cf_to_cr(args.forcestorunner[0])


if __name__ == "__main__":
    main()
