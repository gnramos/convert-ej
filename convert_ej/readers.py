#  -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import os
import re
import xml.etree.ElementTree as ET
import zipfile

try:
    import problem
except:
    from . import problem

class Reader(ABC):
    """Abstract class for reading an E-judge problem."""
    @abstractmethod
    def _read_aux_files(self):
        pass

    @abstractmethod
    def _read_description(self):
        pass

    @abstractmethod
    def _read_examples(self):
        pass

    @abstractmethod
    def _read_id(self):
        pass

    @abstractmethod
    def _read_input(self):
        pass

    @abstractmethod
    def _read_output(self):
        pass

    @abstractmethod
    def _read_limits(self):
        pass

    @abstractmethod
    def _read_notes(self):
        pass

    @abstractmethod
    def _read_solutions(self):
        pass

    @abstractmethod
    def _read_tags(self):
        pass

    @abstractmethod
    def _read_tests(self):
        pass

    @abstractmethod
    def _read_title(self):
        pass

    @abstractmethod
    def _read_tutorial(self):
        pass

    def read(self, file):
        """Return a Problem from the information in the given file."""
        statement = problem.Statement(self._read_title(),
                                      self._read_description(),
                                      self._read_input(),
                                      self._read_output(),
                                      self._read_examples(),
                                      self._read_aux_files(),
                                      self._read_tags(),
                                      self._read_tutorial(),
                                      self._read_notes())
        evaluation = problem.Evaluation(self._read_tests(),
                                        self._read_solutions(),
                                        self._read_limits())
        return problem.Problem(self._read_id(), statement, evaluation)


class ZipReader(Reader):
    """Abstract file for reading an E-judge problem from a zip file."""
    def _get_in_zip(self, file):
        try:
            with self.pzip.open(file) as f:
                return f.read().decode('utf-8')
        except KeyError as e:
            raise ValueError(e)

    def read(self, file):
        """
        Keyword arguments:
        file -- the file containing the data for the problem
        """
        try:
            with zipfile.ZipFile(file) as pzip:
                self.pzip = pzip
                return super().read(file)

        except zipfile.BadZipFile as e:
            raise ValueError(f'{e}')


class BOCA(ZipReader):
    """Reads a BOCA problem from file and returns it as an Problem.

    http://bombonera.org/

    Keep in mind that:
      - BOCA doesn't have a defaut structure for the text, so it's assumed that
        the text is in the "tex" folder, where Statement info is split into
        separate files, just like a boca file when written. (melhorar)

    Keyword arguments:
    file -- the file containing the data for the problem
    """
    def _read_aux_files(self):
        aux_files = {}
        for entry in self.pzip.namelist():
            if entry.startswith('tex/') and not self.pzip.getinfo(entry).is_dir():
                entry_name = os.path.split(entry)[-1].lower()
                if not entry_name.endswith(('.tex', '.cls', 'examples.csv')):
                    with self.pzip.open(entry) as f:
                        aux_files[entry_name] = f.read()

        return aux_files

    def _read_description(self):
        return self._read_stmt_tex('description')

    def _read_examples(self):
        examples = {}
        for num in self._get_in_zip('tex/examples.csv').split(','):
            examples[num] = {}
            examples[num]['in'] = self._get_in_zip(f'input/{num}')
            examples[num]['out'] = self._get_in_zip(f'output/{num}')

        return [examples[k] for k in sorted(examples.keys())]

    def _read_id(self):
        info = self._get_in_zip('description/problem.info').split('\n')
        return info[0].split('=')[1]

    def _read_input(self):
        return self._read_stmt_tex('input')

    def _read_output(self):
        return self._read_stmt_tex('output')

    def _read_limits(self):
        def get_limits(file):
            limits = self._get_in_zip(f'limits/{file}')
            (time_sec, num_repetitions, memory_MB,
             maxfilesize_KB) = re.findall(r'echo (\d+)', limits)
            return {'time_sec': int(time_sec),
                    'memory_MB': int(memory_MB),
                    'maxfilesize_KB': int(maxfilesize_KB)}

        def try_for_python():
            for version in ['', '3', '2']:  # this order matters
                try:
                    limits = get_limits(f'py{version}')
                    return limits
                except ValueError:
                    continue
            else:
                raise ValueError('Limits not found.')

        for entry in self.pzip.namelist():
            if entry.lower().startswith(f'solutions/main'):
                _, ext = os.path.splitext(entry)
                ext = ext[1:]  # remove leading '.'
                return try_for_python() if ext == 'py' else get_limits(ext)
        else:
            raise ValueError('Limits not found.')

    def _read_notes(self):
        return self._read_stmt_tex('notes')

    def _read_solutions(self):
        def source(tag):
            return {os.path.splitext(entry)[1][1:]: self._get_in_zip(entry)
                    for entry in self.pzip.namelist()
                    if entry.lower().startswith(f'solutions/{tag}')}

        return [source('main'), source('accepted')]

    def _read_stmt_tex(self, name):
        file = os.path.join('tex', f'{name}.tex')
        try:
            return self._get_in_zip(file).strip()
        except Exception as e:
            if name not in ['notes', 'tutorial']:
                raise e

        print(f'\t{file} not in zip.')
        return ''

    def _read_tags(self):
        return [tag.strip()
                for tag in self._get_in_zip('description/tags.csv').split(',')
                if tag.strip()]

    def _read_tests(self):
        test_files = [os.path.split(entry)[-1]
                      for entry in self.pzip.namelist()
                      if entry.startswith('input/') and entry != 'input/']

        test_samples = self._get_in_zip('tex/examples.csv').split(',')

        tests = {'examples': {}, 'hidden': {}}
        for name in sorted(test_files):
            test = 'examples' if (name in test_samples) else 'hidden'
            tests[test][name] = {'in': self._get_in_zip(f'input/{name}'),
                                 'out': self._get_in_zip(f'output/{name}')}
        return tests

    def _read_title(self):
        info = self._get_in_zip('description/problem.info').split('\n')
        return info[1].split('=')[1]

    def _read_tutorial(self):
        return self._read_stmt_tex('tutorial')


class Polygon(ZipReader):
    def _get_root(self):
        if self.root is None:
            with self.pzip.open('problem.xml') as f:
                self.root = ET.parse(f).getroot()

        return self.root

    def _read_aux_files(self):
        aux_files = {}
        path = os.path.join('statement-sections', self.stmt_lang)
        for entry in self.pzip.namelist():
            if not self.pzip.getinfo(entry).is_dir() and entry.startswith(path):
                entry_name = os.path.split(entry)[1].lower()
                if not (entry_name.startswith('example.') or
                        entry_name.endswith('.tex')):
                    with self.pzip.open(entry) as f:
                        aux_files[entry_name] = f.read()

        return aux_files

    def _read_description(self):
        return self._read_stmt_tex('legend')

    def _read_examples(self):
        examples = {}
        path = os.path.join('statement-sections', self.stmt_lang)
        for entry in self.pzip.namelist():
            if not self.pzip.getinfo(entry).is_dir() and entry.startswith(path):
                entry_name = os.path.split(entry)[1]
                if entry_name.startswith('example.'):
                    ex = entry_name.split('.')[1]
                    if ex not in examples:
                        examples[ex] = {}
                    if entry_name.endswith('.a'):
                        examples[ex]['out'] = self._get_in_zip(entry)
                    else:
                        examples[ex]['in'] = self._get_in_zip(entry)

        return [examples[k] for k in sorted(examples.keys())]

    def _read_id(self):
        return self._get_root().attrib['short-name']

    def _read_input(self):
        return self._read_stmt_tex('input')

    def _read_output(self):
        return self._read_stmt_tex('output')

    def _read_limits(self):
        testset = self._get_root().find('judging/testset')
        time_msec = int(testset.find('time-limit').text)
        memory_B = int(testset.find('memory-limit').text)
        maxfilesize_KB = 64  # defaut value

        return {'time_sec': time_msec // 1000,
                'memory_MB': memory_B // (2 ** 20),
                'maxfilesize_KB': maxfilesize_KB}

    def _read_notes(self):
        return self._read_stmt_tex('notes')

    def _read_solutions(self):
        def src(attr):
            attr = attr.split('.')[0]
            return 'py' if attr == 'python'else attr

        def source(tag):
            return {src(e.attrib['type']): self._get_in_zip(e.attrib['path'])
                    for e in self._get_root().findall(
                        f'assets/solutions/solution[@tag="{tag}"]/source')}

        return [source('main'), source('accepted')]

    def _read_stmt_tex(self, name):
        file = os.path.join('statement-sections', self.stmt_lang, f'{name}.tex')
        try:
            return self._get_in_zip(file).strip()
        except Exception as e:
            if name not in ['notes', 'tutorial']:
                raise e

        print(f'\t{file} not in zip.')
        return ''

    def _read_tags(self):
        return [tag for tag in self._get_in_zip('tags').splitlines()]

    def _read_tests(self):
        test_files = [entry
                      for entry in self.pzip.namelist()
                      if entry.startswith('tests/') and entry != 'tests/'
                      and not entry.endswith('.a')]
        test_samples = ['sample' in e.attrib
                        for e in self._get_root().findall(
                            'judging/testset/tests/test')]

        # Tests listed in the XML in the same order as the files are
        # numbered.
        tests = {'examples': {}, 'hidden': {}}
        for path, is_sample in zip(sorted(test_files), test_samples):
            test = 'examples' if is_sample else 'hidden'
            file = os.path.split(path)[-1]
            tests[test][file] = {'in': self._get_in_zip(path),
                                 'out': self._get_in_zip(f'{path}.a')}

        return tests

    def _read_title(self):
        return self._read_stmt_tex('name')

    def _read_tutorial(self):
        return self._read_stmt_tex('tutorial')

    def read(self, file, stmt_lang='english'):
        """Reads a polygon problem from file and returns it as an Problem.

        Keyword arguments:
        file -- the file containing the data for the problem
        stmt_lang -- the language the statement of the problem is written in.
        """
        self.stmt_lang = stmt_lang
        self.root = None
        return super().read(file)
