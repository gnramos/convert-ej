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
        if os.path.isdir(self.img_path):
            shutil.rmtree(self.img_path)

    def get_data(self, problem):
        if problem.text.images:
            shutil.copytree(problem.text.img_path, self.img_path)
            problem.text.img_path = self.img_path
        self.problem = problem

    def read(self, file):
        """Read the data from the given file.

        Returns a CompetitiveProgrammingProblem.
        """
        raise NotImplementedError

    def write(self, file=None):
        """Write the data into the given file."""

        def CDATA(text=None):
            '''
            Includes the CDATA tag
            '''
            element = ET.Element('![CDATA[')
            element.text = text
            return element

        ET._original_serialize_xml = ET._serialize_xml

        def _serialize_xml(write, elem, qnames, namespaces,
                           short_empty_elements, **kwargs):
            '''
            New serializing function to deal with the CDATA tag
            '''
            if elem.tag == '![CDATA[':
                write("\n<{}{}]]>\n".format(elem.tag, elem.text))
            else:
                return ET._original_serialize_xml(
                       write, elem, qnames, namespaces, short_empty_elements,
                       **kwargs)

        ET._serialize_xml = ET._serialize['xml'] = _serialize_xml

        def get_templates(package_dir):
            tree = ET.parse(os.path.join(package_dir, 'Template.xml'))
            root = tree.getroot()
            root = root[0]
            return [tree, root]

        def get_test_templates(package_dir):
            test_tree = ET.parse(os.path.join(package_dir,
                                 'Testcase-Template.xml'))
            test_root = test_tree.getroot()
            return [test_tree, test_root]

        def insert_text(text, root):

            def get_section(header, description):
                return '{}<p>\n{}\n</p>\n'.format(header,
                                                  tex2html(description))

            root.find("name").find("text").text = text.name

            sections = [
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

            def insert_images(root, images, img_path):
                try:
                    convert_eps_to_png(img_path)
                except Exception:
                    raise Exception('Could not convert the .eps image.\n\
                This can be solved by acessing:\n\"/etc/ImageMagick-6/policy.xml\"\n\
                and commenting the line:\n\
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
                shutil.rmtree(img_path)

            insert_images(root, self.problem.text.images,
                          self.problem.text.img_path)

        def insert_testcases(test_cases, root, package_dir):

            for t_in, t_out in zip(test_cases['example']['in'],
                                   test_cases['example']['out']):
                [test_tree, test_root] = get_test_templates(package_dir)

                test_root.find("stdin").find("text").text = t_in
                test_root.find("expected").find("text").text = t_out
                test_root.set("useasexample", "1")
                root.find("testcases").append(test_root)

            for t_in, t_out in zip(test_cases['hidden']['in'],
                                   test_cases['hidden']['out']):
                [test_tree, test_root] = get_test_templates(package_dir)

                test_root.find("stdin").find("text").text = t_in
                test_root.find("expected").find("text").text = t_out
                test_root.set("useasexample", "0")
                root.find("testcases").append(test_root)

        def insert_solution(solution, root):
            root.find("answer").append(CDATA(solution))

        def insert_solution_type(sol_type, root):
            if sol_type.startswith('c.'):
                ans = 'c_program'
            elif sol_type.startswith('cpp.'):
                ans = 'cpp_program'
            elif sol_type.startswith('python.'):
                ans = 'python3'
            else:
                raise Exception("Solution type not identified.")
            root.find("coderunnertype").text = ans

        def insert_tutorial(tutorial, root):
            if tutorial:
                root.find("generalfeedback").find("text").text = \
                    tex2html(tutorial)

        def insert_tags(taglist, root):
            tags = root.find("tags")
            for tag in taglist:
                tag_element = ET.Element('tag')
                ET.SubElement(tag_element, 'text').text = tag
                tags.append(tag_element)

        def insert_time_limit(time_limit, root):
            root.find("cputimelimitsecs").text = str(time_limit)

        def insert_memory_limit(memory_limit, root):
            root.find("memlimitmb").text = str(memory_limit)

        def insert_penalty(penalty, root):
            root.find("penaltyregime").text = str(penalty)

        def insert_all_or_nothing(all_or_nothing, root):
            root.find("allornothing").text = '1' if all_or_nothing else '0'

        def write_xml_file(tree, question_name):
            files = 'files'
            if not os.path.exists(files):
                os.mkdir(files)
            tree.write(os.path.join(files, question_name + '.xml'), 'UTF-8')

        if not self.problem:
            raise Exception('Intermediate class not found.')

        package_dir = os.path.abspath(os.path.dirname(__file__))
        [tree, root] = get_templates(package_dir)

        insert_text(self.problem.text, root)
        insert_tutorial(self.problem.text.tutorial, root)
        insert_solution(self.problem.solutions, root)
        insert_testcases(self.problem.test_cases, root, package_dir)
        insert_solution_type(self.problem.sol_type, root)
        insert_tags(self.problem.tags, root)
        insert_time_limit(self.problem.time_limit, root)
        insert_memory_limit(self.problem.memory_limit, root)
        insert_penalty(self.penalty, root)
        insert_all_or_nothing(self.all_or_nothing, root)

        write_xml_file(tree, self.problem.handle)
