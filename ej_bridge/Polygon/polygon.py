#  -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import zipfile

# Import problem.py classes.
import sys
sys.path.append('..')
from problem import Converter, EJudgeProblem, Evaluation, Statement


class Polygon(Converter):
    """Class for converting problems to/from Polygon.

    https://polygon.codeforces.com/

    Files from Polygon must be generated from a "full package", and the zip
    must be the "Linux" version in order to include all test files.
    """

    def add_dest_parser(self, parser):
        """Adds a parser for creating a file formatted for a Polygon EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        raise NotImplementedError

    def add_origin_parser(self, parser):
        """Adds a parser for creating an EJudgeProblem from a file formatted
        for a Polygon EJudge.

        Keyword arguments:
        parser -- the parser to configure
        """
        pass

    def read(self, file, args, language='english'):
        """Reads a problem from file and returns it as an EJudgeProblem.

        Keyword arguments:
        file -- the file containing the data for the problem
        args -- the arguments for configuring the EJudgeProblem
        language -- the language the statement of the problem is written in.
        """
        def get_images_and_examples():
            images = {}
            examples = {}
            path = os.path.join('statement-sections', language)
            for entry in pzip.namelist():
                if not pzip.getinfo(entry).is_dir() and entry.startswith(path):
                    entry_name = os.path.split(entry)[1]
                    if entry_name.startswith('example.'):
                        ex = entry_name.split('.')[1]
                        if ex not in examples:
                            examples[ex] = {}
                        if entry_name.endswith('.a'):
                            examples[ex]['out'] = get_in_zip(entry)
                        else:
                            examples[ex]['in'] = get_in_zip(entry)
                    elif not entry_name.lower().endswith('.tex'):
                        with pzip.open(entry) as f:
                            images[entry_name] = f.read()

            return images, [examples[k] for k in sorted(examples.keys())]

        def get_in_zip(file):
            try:
                with pzip.open(file) as f:
                    return f.read().decode('utf-8')
            except KeyError:
                return ''

        def get_limits():
            testset = root.find('judging/testset')
            time_msec = int(testset.find('time-limit').text)
            memory_B = int(testset.find('memory-limit').text)

            return {'time_sec': time_msec // 1000,
                    'memory_MB': memory_B // (2 ** 20)}

        def get_stmt_tex(name):
            file = os.path.join('statement-sections', language, f'{name}.tex')
            return get_in_zip(file).rstrip('\n')

        def get_tags():
            return [e.attrib['value'] for e in root.findall('tags/tag')]

        def get_solutions():
            def src(attr):
                attr = attr.split('.')[0]
                return 'py' if attr == 'python'else attr

            def solution_code(tag):
                return {src(e.attrib['type']): get_in_zip(e.attrib['path'])
                        for e in root.findall(
                            f'assets/solutions/solution[@tag="{tag}"]/source')}

            return [solution_code('main'), solution_code('accepted')]

        def get_tests():
            test_files = [entry
                          for entry in pzip.namelist()
                          if entry.startswith('tests/') and entry != 'tests/'
                          and not entry.endswith('a')]
            test_samples = ['sample' in e.attrib
                            for e in root.findall(
                                'judging/testset/tests/test')]

            # Tests listed in the XML in the same order as the files are
            # numbered.
            tests = {'examples': {}, 'hidden': {}}
            for path, is_sample in zip(sorted(test_files), test_samples):
                test = 'examples' if is_sample else 'hidden'
                file = os.path.split(path)[-1]
                tests[test][file] = {'in': get_in_zip(path),
                                     'out': get_in_zip(f'{path}.a')}

            return tests

        try:
            with zipfile.ZipFile(file) as pzip:
                with pzip.open('problem.xml') as f:
                    root = ET.parse(f).getroot()

                problem_id = root.attrib['short-name']

                images, examples = get_images_and_examples()
                statement = Statement(get_stmt_tex('name'),
                                      get_stmt_tex('legend'),
                                      get_stmt_tex('input'),
                                      get_stmt_tex('output'),
                                      examples,
                                      images,
                                      get_tags(),
                                      get_stmt_tex('tutorial'),
                                      get_stmt_tex('notes'))

                evaluation = Evaluation(get_tests(),
                                        get_solutions(),
                                        get_limits())
        except zipfile.BadZipFile as e:
            raise ValueError(f'{e}')

        return EJudgeProblem(problem_id, statement, evaluation)

    def write(self, problem, args):
        """Writes the given EJudgeProblem into a Polygon file.

        Keyword arguments:
        problem -- the EJudgeProblem containing the data for the problem
        args -- the arguments for configuring the created file
        """
        raise NotImplementedError
