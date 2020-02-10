from .utils import EJudge, ProblemText, CompetitiveProgrammingProblem as Cpp

import os
import shutil
import xml.etree.ElementTree as ET
import zipfile


class CodeForces(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __init__(self, language=None, file=None):
        self.language = language
        self.img_path = 'images_cf'
        super().__init__(file)

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())

    def __del__(self):
        """Delete the image path and the unziped path, if they exist."""
        if os.path.isdir(self.img_path):
            shutil.rmtree(self.img_path)
        if os.path.isdir(self.package_dir):
            shutil.rmtree(self.package_dir)

    def read_data(self, problem):
        """Read the data from the other class, and create a new image path."""
        raise NotImplementedError

    def read(self, file):
        """Read the data from the given file."""

        def read_problem_xml(package_dir):
            xml = os.path.join(package_dir, 'problem.xml')
            if not os.path.isfile(xml):
                raise Exception('{} is not a file.'.format(xml))

            tree = ET.parse(xml)
            root = tree.getroot()

            return tree, root

        def unzip(package):
            """Unzip the file and return the path to it."""
            if not os.path.isfile(package):
                raise Exception('{} is not a file.'.format(package))
            if not package.endswith('.zip'):
                raise Exception('{} is not a zip file.'.format(package))

            file_dir, file_name = os.path.split(package)
            package_dir = os.path.splitext(file_name)[0]

            with zipfile.ZipFile(package, 'r') as zip_file:
                zip_file.extractall(package_dir)

            return package_dir

        def read_text(package_dir, img_path):
            """Read data and build a ProblemText class with it.

            Return a ProblemText class.
            """
            def read_images(sections, img_path):
                """Copy the images into a temporary path, if they exist.

                Return a list with the name of the images files.
                """
                images = []
                try:
                    if not os.path.exists(img_path):
                        os.mkdir(img_path)

                    with os.scandir(sections) as it:
                        for entry in it:
                            if entry.is_file() and \
                                    entry.name.endswith(('.png', 'jpg',
                                                         '.eps')):
                                shutil.move(os.path.join(sections, entry.name),
                                            os.path.join(img_path, entry.name))
                                images.append(entry.name)
                except Exception:
                    raise Exception('Could not open the images.')
                return images

            sections = os.path.join(package_dir,
                                    'statement-sections',
                                    'english')
            try:
                with open(os.path.join(sections, 'name.tex')) as f:
                    name = f.read()
                with open(os.path.join(sections, 'legend.tex')) as f:
                    legend = f.read()
                with open(os.path.join(sections, 'input.tex')) as f:
                    input = f.read()
                with open(os.path.join(sections, 'output.tex')) as f:
                    output = f.read()
                if os.path.isfile(os.path.join(sections, 'notes.tex')):
                    with open(os.path.join(sections, 'notes.tex')) as f:
                        notes = f.read()
                else:
                    notes = None
                if os.path.isfile(os.path.join(sections, 'tutorial.tex')):
                    with open(os.path.join(sections, 'tutorial.tex')) as f:
                        tutorial = f.read()
                else:
                    tutorial = None
            except Exception:
                raise Exception('Could not open a text file.')

            images = read_images(sections, img_path)

            return ProblemText(name, legend, input, output, tutorial,
                               images, img_path, notes)

        def read_tests(root):
            """Read the tests cases using the problem.xml file.

            Return lists with inputs and outputs tests.
            """
            def load_file(file):
                """Read a file and return it's content."""
                if not os.path.isfile(file):
                    raise Exception('{} is not a file.'.format(file))
                with open(file) as f:
                    content = f.read()
                return content

            examples = {'in': [], 'out': []}
            hidden = {'in': [], 'out': []}
            x = 1
            for e in root.findall('judging/testset/tests/test'):
                file_num = '{:0>2}'.format(x)
                file = os.path.join(package_dir, 'tests', file_num)
                if 'sample' in e.attrib:
                    examples['in'].append(load_file(file))
                    examples['out'].append(load_file(file + '.a'))
                else:
                    hidden['in'].append(load_file(file))
                    hidden['out'].append(load_file(file + '.a'))

                x += 1

            return {'example': examples, 'hidden': hidden}

        def read_limits(root):
            """Read the time and memoty limits and return them."""
            testset = root.find('judging/testset')
            time_limit = testset.find('time-limit').text
            memory_limit = testset.find('memory-limit').text

            return int(time_limit) // 1000, int(memory_limit) // (2 ** 20)

        def read_main_solution(package_dir, root, language):
            """Find the solution specified by a type parameter (language)
            and return them."""
            for e in root.findall(
                    'assets/solutions/solution[@tag="main"]/source'):
                if(e.attrib['type'].startswith(language+'.')):
                    main_file = e.attrib['path']
                    sol_type = e.attrib['type']
                    break
            else:
                for e in root.findall(
                        'assets/solutions/solution[@tag="accepted"]/source'):
                    if(e.attrib['type'].startswith(language+'.')):
                        main_file = e.attrib['path']
                        sol_type = e.attrib['type']
                        break
                else:
                    raise Exception('{} solution not found.'.format(language))

            with open(os.path.join(package_dir, main_file), 'r') as f:
                source = f.read()
            return source, sol_type

        def read_tags(root):
            """Read the tags and return them on a list."""
            return [e.attrib['value'] for e in root.findall('tags/tag')]

        package_dir = unzip(file)

        self.package_dir = package_dir

        tree, root = read_problem_xml(package_dir)
        handle = root.attrib['short-name']
        text = read_text(package_dir, self.img_path)
        tests_files = read_tests(root)
        time_limit_sec, memory_limit_mb = read_limits(root)
        main_source, sol_type = read_main_solution(package_dir,
                                                   root, self.language)
        tags = read_tags(root)

        self.problem = Cpp(handle, text, tests_files, main_source,
                           sol_type, tags, memory_limit_mb, time_limit_sec)

    def write(self, file=None):
        """Write the given data into a file."""

        raise NotImplementedError
