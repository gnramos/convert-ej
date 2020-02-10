from .utils import EJudge, tex2html, convert_eps_to_png

from base64 import b64encode
import xml.etree.ElementTree as ET
import os
import shutil


class CodeRunner(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __init__(self, penalty=None, all_or_nothing=None, file=None):
        self.penalty = penalty
        self.all_or_nothing = all_or_nothing
        self.img_path = 'images_cr'
        super().__init__(file)

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())

    def __del__(self):
        """Delete the image path."""
        if os.path.isdir(self.img_path):
            shutil.rmtree(self.img_path)

    def read_data(self, problem):
        """Read the data from the other class, and create a new image path."""
        if problem.text.images:
            shutil.copytree(problem.text.img_path, self.img_path)
            problem.text.img_path = self.img_path
        self.problem = problem

    def read(self, file):
        """Read the data from the given file."""
        raise NotImplementedError

    def write(self, file=None):
        """Write the given data into a file."""

        def CDATA(text=None):
            """Includes the CDATA tag."""

            element = ET.Element('![CDATA[')
            element.text = text
            return element

        # Save the original method.
        ET._original_serialize_xml = ET._serialize_xml

        def _serialize_xml(write, elem, qnames, namespaces,
                           short_empty_elements, **kwargs):
            """New serializing method to deal with the CDATA tag."""
            if elem.tag == '![CDATA[':
                write("\n<{}{}]]>\n".format(elem.tag, elem.text))
            else:
                return ET._original_serialize_xml(
                       write, elem, qnames, namespaces, short_empty_elements,
                       **kwargs)

        # Set the new method as the standard one.
        ET._serialize_xml = ET._serialize['xml'] = _serialize_xml

        def read_templates(package_dir):
            """Read the template from the package path.

            Return the ElementTree elements with the template
            """
            tree = ET.parse(os.path.join(package_dir, 'Template.xml'))
            root = tree.getroot()
            root = root[0]
            return tree, root

        def read_test_templates(package_dir):
            """Read the testcase template from the package path.

            Return the ElementTree elements with the template
            """
            test_tree = ET.parse(os.path.join(package_dir,
                                 'Testcase-Template.xml'))
            test_root = test_tree.getroot()
            return test_tree, test_root

        def write_text(text, root):
            """Write the text on the root element."""
            def get_section(header, description):
                """Return a formated description, given a header."""
                return '{}<p>\n{}\n</p>\n'.format(header,
                                                  tex2html(description))

            root.find("name").find("text").text = text.name

            sections = [  # Header, description.
                ('context', ''),
                ('input', '\n<p>\n<b>Entrada</b><br /></p>\n'),
                ('output', '\n<p>\n<b>Saida</b><br /></p>\n'),
                ('notes', '\n<p>\n<b>Notas</b><br /></p>\n'),
            ]
            texto = ''

            for attr_name, header in sections:
                if getattr(text, attr_name):
                    texto += get_section(header, getattr(text, attr_name))

            root.find("questiontext").find("text").append(CDATA(texto))

            def write_images(root, images, img_path):
                """Convert the images to the base64 format, and write them on the root element.

                Convert the .eps images to .png, using the ImageMagick function
                convert.
                """
                try:
                    convert_eps_to_png(img_path)
                except Exception:
                    raise Exception('Could not convert the .eps image.\n\
                This can be solved by acessing:\n\
                \"/etc/ImageMagick-6/policy.xml\"\nand commenting the line:\n\
                \"<policy domain="coder" rights="none" pattern="PS" />\"\n\
                For more information: https://stackoverflow.com/questions/52998331/imagemagick\
                -security-policy-pdf-blocking-conversion')

                for name in images:
                    if name.endswith('.eps'):
                        file_name, file_ext = os.path.splitext(name)
                        name = file_name + '.png'

                    path = os.path.join(img_path, name)

                    img = ET.Element('file')
                    img.set('name', name)
                    img.set('path', '/')
                    img.set('encoding', 'base64')

                    with open(path, "rb") as image:
                        encoded_string = str(b64encode(image.read()), 'utf-8')

                    img.text = encoded_string
                    root.find("questiontext").append(img)

            write_images(root, self.problem.text.images,
                         self.problem.text.img_path)

        def write_testcases(test_cases, root, package_dir):
            """Write the testcases on the root element."""
            for t_in, t_out in zip(test_cases['example']['in'],
                                   test_cases['example']['out']):
                test_tree, test_root = read_test_templates(package_dir)

                test_root.find("stdin").find("text").text = t_in
                test_root.find("expected").find("text").text = t_out
                test_root.set("useasexample", "1")
                root.find("testcases").append(test_root)

            for t_in, t_out in zip(test_cases['hidden']['in'],
                                   test_cases['hidden']['out']):
                test_tree, test_root = read_test_templates(package_dir)

                test_root.find("stdin").find("text").text = t_in
                test_root.find("expected").find("text").text = t_out
                test_root.set("useasexample", "0")
                root.find("testcases").append(test_root)

        def write_solution(solution, root):
            """Write the solution on the root element."""
            root.find("answer").append(CDATA(solution))

        def write_solution_type(sol_type, root):
            """Write the solution type on the root element."""
            if sol_type.startswith('c.'):
                ans = 'c_program'
            elif sol_type.startswith('cpp.'):
                ans = 'cpp_program'
            elif sol_type.startswith('python.'):
                ans = 'python3'
            else:
                raise Exception("Solution type not identified.")
            root.find("coderunnertype").text = ans

        def write_tutorial(tutorial, root):
            """Write the tutorial on the root element."""
            if tutorial:
                root.find("generalfeedback").find("text").text = \
                    tex2html(tutorial)

        def write_tags(taglist, root):
            """Write the tags on the root element."""
            tags = root.find("tags")
            for tag in taglist:
                tag_element = ET.Element('tag')
                ET.SubElement(tag_element, 'text').text = tag
                tags.append(tag_element)

        def write_time_limit(time_limit, root):
            """Write the time limit on the root element."""
            root.find("cputimelimitsecs").text = str(time_limit)

        def write_memory_limit(memory_limit, root):
            """Write the memoty limit on the root element."""
            root.find("memlimitmb").text = str(memory_limit)

        def write_penalty(penalty, root):
            """Write the penalty parameter on the root element."""
            root.find("penaltyregime").text = str(penalty)

        def write_all_or_nothing(all_or_nothing, root):
            """Write the all or nothing parameter on the root element."""
            root.find("allornothing").text = '1' if all_or_nothing else '0'

        def write_xml_file(tree, question_name):
            """Write the .xml file on the files directory."""
            files = 'files'

            if not os.path.exists(files):
                os.mkdir(files)
            tree.write(os.path.join(files, question_name + '.xml'), 'UTF-8')

        if not self.problem:
            raise Exception('Intermediate class not found.')

        package_dir = os.path.abspath(os.path.dirname(__file__))
        tree, root = read_templates(package_dir)

        write_text(self.problem.text, root)
        write_tutorial(self.problem.text.tutorial, root)
        write_solution(self.problem.solutions, root)
        write_testcases(self.problem.test_cases, root, package_dir)
        write_solution_type(self.problem.sol_type, root)
        write_tags(self.problem.tags, root)
        write_time_limit(self.problem.time_limit, root)
        write_memory_limit(self.problem.memory_limit, root)
        write_penalty(self.penalty, root)
        write_all_or_nothing(self.all_or_nothing, root)

        write_xml_file(tree, self.problem.handle)

        # Set the standard method as the original one.
        ET._serialize_xml = ET._serialize['xml'] = ET._original_serialize_xml
