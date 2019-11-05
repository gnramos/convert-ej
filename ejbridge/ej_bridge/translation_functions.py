import os
import zipfile
import shutil
from .coderunner import intermediate_to_coderunner


def dir_cf_to_cr(directory):
    questions = os.listdir(directory)
    for name in questions:
        if name.endswith('.zip'):
            with zipfile.ZipFile(directory + '/' + name, 'r') as zip_ref:
                zip_ref.extractall('tmp')
            intermediate_to_coderunner('tmp', name[:-4])
            shutil.rmtree('tmp')
