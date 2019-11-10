import os
import zipfile
import shutil
from .codeforces import codeforces_to_intermediate
from .coderunner import intermediate_to_coderunner


def dir_cf_to_cr(dir):
    questions = os.listdir(dir)
    for name in questions:
        if name.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(dir, name), 'r') as zip_ref:
                zip_ref.extractall('tmp')
            codeforces_to_intermediate('tmp', name[:-4])
            intermediate_to_coderunner(os.path.join('intermadiate_files/',
                                                    name[:-4]), name[:-4])
            shutil.rmtree('tmp')
