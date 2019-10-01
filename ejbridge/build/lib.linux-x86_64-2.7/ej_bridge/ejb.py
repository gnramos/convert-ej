import argparse
from .coderunner import xml_gen, dir_xml_gen


def main():

    parser = argparse.ArgumentParser(description="EJBridge")

    parser.add_argument("-d", "--directory", type=str, nargs=1, default=None,
                        help="Directory name with all the questions")

    parser.add_argument("-q", "--question", type=str, nargs=1, default=None,
                        help="Name of the question")

    args = parser.parse_args()

    if args.question:
        xml_gen(args.question[0], args.question[0])
    elif args.directory:
        dir_xml_gen(args.directory[0])


if __name__ == "__main__":
    main()
