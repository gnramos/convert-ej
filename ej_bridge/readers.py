#  -*- coding: utf-8 -*-

import os
import problem
import xml.etree.ElementTree as ET
import zipfile


def boca(file):
    """Reads a BOCA problem from file and returns it as an EJudgeProblem.

    http://bombonera.org/

    Keep in mind that:
      - BOCA doesn't have a defaut structure for the text, so it's assumed that
        the text is in the "tex" folder, where Statement info is split into
        separate files, just like a boca file when written. (melhorar)

    Keyword arguments:
    file -- the file containing the data for the problem
    """

    def get_in_zip(file):
        try:
            with pzip.open(file) as f:
                return f.read().decode('utf-8')
        except KeyError as e:
            raise ValueError(e)

    def get_images_examples_and_tags():
        images = {}
        examples = {}
        tags = []
        for entry in pzip.namelist():
            if not pzip.getinfo(entry).is_dir() and entry.startswith('tex'):
                entry_name = os.path.split(entry)[1]
                if entry_name == 'examples.csv':
                    exps = get_in_zip(entry).split(',')
                    for num in exps:
                        examples[num] = {}
                        examples[num]['in'] = get_in_zip(f'input/{num}')
                        examples[num]['out'] = get_in_zip(f'output/{num}')
                elif entry_name == 'tags.csv':
                    tags = [x.strip() for x in get_in_zip(entry).split(',')
                            if x.strip()]
                elif not entry_name.lower().endswith('.tex')\
                        and not entry_name.lower().endswith('.cls'):
                    with pzip.open(entry) as f:
                        images[entry_name] = f.read()

        return images, [examples[k] for k in sorted(examples.keys())], tags

    def get_tex(name):
        file = os.path.join('tex', f'{name}.tex')
        try:
            return get_in_zip(file).strip()
        except Exception as e:
            if name not in ['notes', 'tutorial']:
                raise e

        print(f'\t{file} not in zip.')
        return ''

    def get_solutions():
        def solution_code(tag):
            return {os.path.splitext(entry)[1][1:]: get_in_zip(entry)
                    for entry in pzip.namelist()
                    if entry.startswith(f'solutions/{tag}')}

        return [solution_code('main'), solution_code('accepted')]

    def get_tests():
        test_files = [os.path.split(entry)[-1]
                      for entry in pzip.namelist()
                      if entry.startswith('input/') and entry != 'input/']

        test_samples = get_in_zip('tex/examples.csv').split(',')

        tests = {'examples': {}, 'hidden': {}}
        for name in sorted(test_files):
            test = 'examples' if (name in test_samples) else 'hidden'
            tests[test][name] = {'in': get_in_zip(f'input/{name}'),
                                 'out': get_in_zip(f'output/{name}')}
        return tests

    def get_limits():
        # Implementar get_solutions() antes de implementar
        time_msec = 1000
        memory_B = 10000000

        return {'time_sec': time_msec // 1000,
                'memory_MB': memory_B // (2 ** 20)}

    def get_id_and_title():
        info = get_in_zip('description/problem.info').split('\n')
        return info[0].split('=')[1], info[1].split('=')[1]

    try:
        with zipfile.ZipFile(file) as pzip:
            problem_id, title = get_id_and_title()

            images, examples, tags = get_images_examples_and_tags()
            statement = problem.Statement(title,
                                          get_tex('description'),
                                          get_tex('input'),
                                          get_tex('output'),
                                          examples,
                                          images,
                                          tags,
                                          get_tex('tutorial'),
                                          get_tex('notes'))
            evaluation = problem.Evaluation(get_tests(),
                                            get_solutions(),
                                            get_limits())

    except zipfile.BadZipFile as e:
        raise ValueError(f'{e}')

    return problem.EJudgeProblem(problem_id, statement, evaluation)
    return NotImplementedError


def polygon(file, stmt_lang='english'):
    """Reads a polygon problem from file and returns it as an EJudgeProblem.

    Keyword arguments:
    file -- the file containing the data for the problem
    stmt_lang -- the language the statement of the problem is written in.
    """

    def get_in_zip(file):
        try:
            with pzip.open(file) as f:
                return f.read().decode('utf-8')
        except KeyError as e:
            raise ValueError(e)

    def get_images_and_examples():
        images = {}
        examples = {}
        path = os.path.join('statement-sections', stmt_lang)
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

    def get_limits():
        testset = root.find('judging/testset')
        time_msec = int(testset.find('time-limit').text)
        memory_B = int(testset.find('memory-limit').text)

        return {'time_sec': time_msec // 1000,
                'memory_MB': memory_B // (2 ** 20)}

    def get_stmt_tex(name):
        file = os.path.join('statement-sections', stmt_lang, f'{name}.tex')
        try:
            return get_in_zip(file).strip()
        except Exception as e:
            if name not in ['notes', 'tutorial']:
                raise e

        print(f'\t{file} not in zip.')
        return ''

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
                      and not entry.endswith('.a')]
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
            statement = problem.Statement(get_stmt_tex('name'),
                                          get_stmt_tex('legend'),
                                          get_stmt_tex('input'),
                                          get_stmt_tex('output'),
                                          examples,
                                          images,
                                          get_tags(),
                                          get_stmt_tex('tutorial'),
                                          get_stmt_tex('notes'))

            evaluation = problem.Evaluation(get_tests(),
                                            get_solutions(),
                                            get_limits())
    except zipfile.BadZipFile as e:
        raise ValueError(f'{e}')

    return problem.EJudgeProblem(problem_id, statement, evaluation)
