import argparse
from xmlgenerator import xml_gen


def main():

    parser = argparse.ArgumentParser(description="OJBridge")

    parser.add_argument("-d", "--dir", type=str, nargs=1,
                        metavar="name_dir", default=None,
                        help="Directory name")

    args = parser.parse_args()

    xml_gen(args.dir[0])


if __name__ == "__main__":
    main()
