from .utils import EJudge, ProblemText, CompetitiveProgrammingProblem as Cpp

import os
import shutil
import xml.etree.ElementTree as ET
import zipfile


class CodeForces(EJudge):
    """Manipulates CompetitiveProgrammingProblem files."""

    def __init__(self, language=None, file=None):
        super().__init__(file)
        self.language = language

    def __str__(self):
        """Return a readable version of the instance's data."""
        return '\n'.join('{}: {}'.format(k, v) for k, v in vars(self).items())

    def read(self, file):
        """Read the data from the given file.

        Returns a CompetitiveProgrammingProblem.
        """
        def unzip(package):
            assert package.endswith('.zip'), '{} is not a zip file'.format(
                package)

            file_dir, file_name = os.path.split(package)
            package_dir = os.path.splitext(file_name)[0]

            with zipfile.ZipFile(package, 'r') as zip_file:
                zip_file.extractall(package_dir)

            return package_dir

        def cleanup(package_dir):
            shutil.rmtree(package_dir)

        def build_text(package_dir):
            sections = os.path.join(package_dir,
                                    'statement-sections',
                                    'english')
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

            images = []

            return ProblemText(name, legend, input, output, tutorial,
                               images, notes)

        def read_tests(root):
            def load_file(file):
                assert os.path.isfile(file), '{} is not a file'.format(file)
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
            testset = root.find('judging/testset')
            time_limit = testset.find('time-limit').text
            memory_limit = testset.find('memory-limit').text

            return int(time_limit) // 1000, int(memory_limit) // (2 ** 20)

        def read_main_solution(package_dir, root, language):
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
                    raise NameError('Solution not found')

            with open(os.path.join(package_dir, main_file), 'r') as f:
                source = f.read()
            return [source, sol_type]

        def read_tags(root):
            return [e.attrib['value'] for e in root.findall('tags/tag')]

        assert os.path.isfile(file), '{} is not a file'.format(file)
        package_dir = unzip(file)

        xml = os.path.join(package_dir, 'problem.xml')
        assert os.path.isfile(xml), '{} is not a file'.format(xml)

        tree = ET.parse(xml)
        root = tree.getroot()
        handle = root.attrib['short-name']
        text = build_text(package_dir)
        tests_files = read_tests(root)
        time_limit_sec, memory_limit_mb = read_limits(root)
        [main_source, sol_type] = read_main_solution(package_dir,
                                                     root, self.language)
        tags = read_tags(root)

        images = {}
        with os.scandir(os.path.join(package_dir, 'statements',
                                     'english')) as it:
            for entry in it:
                if entry.is_file() and entry.name.endswith(('.png', '.jpg',
                                                            '.eps')):
                    with open(entry.name, 'rb') as f:
                        images[entry.name] = f.read()

        cleanup(package_dir)

        self.problem = Cpp(handle, text, images, tests_files, main_source,
                           sol_type, tags, memory_limit_mb, time_limit_sec)

    def write(self, file=None):
        """Write the data into the given file."""
        assert self.problem

        if file:
            assert not os.path.isfile(file)

        raise NotImplementedError
