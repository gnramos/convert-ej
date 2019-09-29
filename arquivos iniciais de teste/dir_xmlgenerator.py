import os
from xmlgenerator import xml_gen


def dir_xml_gen(directory):
    questions = os.listdir(directory)
    for name in questions:
        xml_gen(directory + '/' + name, name)
