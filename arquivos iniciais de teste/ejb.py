import argparse
from xmlgenerator import xml_gen
from dir_xmlgenerator import dir_xml_gen


def main():

    parser = argparse.ArgumentParser(description="EJBridge")

    parser.add_argument("-d", "--directory", type=str, nargs=1,
                        metavar="name_directory", default=None,
                        help="Directory name with all the questions")

    parser.add_argument("-q", "--question", type=str, nargs=1,
                        metavar="name_question", default=None,
                        help="Name of the the question")

    args = parser.parse_args()

    if args.question:
        xml_gen(args.question[0], args.question[0])
    elif args.directory:
        dir_xml_gen(args.directory[0])


if __name__ == "__main__":
    main()
