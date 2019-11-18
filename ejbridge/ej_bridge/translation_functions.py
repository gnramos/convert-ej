import os
import zipfile
import shutil
from codeforces import codeforces_to_intermediate
from coderunner import intermediate_to_coderunner


def cf2cr(files, penalty, all_or_nothing, language):
    """Process CodeForces packages into CodeRunner XML files."""
    for name in files:
        if name.endswith('.zip'):
            with zipfile.ZipFile(name, 'r') as zip_ref:
                zip_ref.extractall('tmp')

            file_name = os.path.splitext(os.path.split(name)[1])[0]

            check = codeforces_to_intermediate('tmp', file_name, language)
            if not check:
                shutil.rmtree((os.path.join('intermadiate_files', file_name)))
            else:
                intermediate_to_coderunner(os.path.join('intermadiate_files',
                                                        file_name), file_name,
                                           penalty, all_or_nothing)
            shutil.rmtree('tmp')
            shutil.rmtree('intermadiate_files')
