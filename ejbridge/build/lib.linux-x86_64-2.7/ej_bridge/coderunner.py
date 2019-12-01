from .utils import EJudge

import xml.etree.ElementTree as ET
import os


class CodeRunner(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __init__(self, penalty=None, all_or_nothing=None,
                 language=None, file=None):
        super().__init__(file)
        self.penalty = penalty
        self.all_or_nothing = all_or_nothing
        self.language = language

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())

    def read(self, file):
        """Read the data from the given file.

        Returns a CompetitiveProgrammingProblem.
        """
        raise NotImplementedError

    def write(self, file=None):
        """Write the data into the given file."""

        def get_templates(package_dir):
            tree = ET.parse(os.path.join(package_dir, 'Template.xml'))
            root = tree.getroot()
            root = root[0]
            test_tree = ET.parse(os.path.join(package_dir,
                                 'Testcase-Template.xml'))
            test_root = test_tree.getroot()
            return [tree, root, test_tree, test_root]

        def insert_tags(taglist, root):
            tags = root.find("tags")
            for tag in taglist:
                tag_element = ET.Element('tag')
                ET.SubElement(tag_element, 'text').text = tag
                tags.append(tag_element)

        def write_xml_file(tree, question_name):
            files = 'files'
            if not os.path.exists(files):
                os.mkdir(files)
            tree.write(os.path.join(files, question_name + '.xml'), 'UTF-8')

        assert self.problem

        package_dir = os.path.abspath(os.path.dirname(__file__))
        [tree, root, test_tree, test_root] = get_templates(package_dir)

        # insert_texts(root)
        # convert_eps_to_png()
        # insert_images(root)
        # insert_tutorial(root)
        # insert_solution_type(directory, root)
        # insert_solution(directory, root)
        # insert_testcases(directory, root, test_root, package_dir)
        insert_tags(self.problem.tags, root)
        # insert_time_limit(directory, root)
        # insert_memory_limit(directory, root)
        # insert_penalty(root, penalty)
        # insert_all_or_nothing(root, all_or_nothing)

        write_xml_file(tree, self.problem.handle)
