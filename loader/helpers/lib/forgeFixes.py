import os
import fileinput
import requests
import zipfile
import distutils.dir_util
import tempfile

patchfiles = 'gdn/static/cache/forgepatch01'


def patchForge(path):

    if not os.path.exists(patchfiles):
        print('Downloading forgepatch')
        r = requests.get('http://s3.amazonaws.com/SpaceZips/forgepatch.zip',
                         stream=True)

        handle, temp_file_path = tempfile.mkstemp()

        with open(temp_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

        with zipfile.ZipFile(temp_file_path) as z:
            z.extractall(patchfiles)

        os.remove(temp_file_path)

    distutils.dir_util.copy_tree(patchfiles, path)


def modify(path, build):
    patchForge(path)

    config = os.path.join(path, 'config/forge.cfg')
    replacements = {
        'removeErroringEntities=false': 'removeErroringEntities=true',
        'removeErroringTileEntities=false': 'removeErroringTileEntities=true'
    }

    if not os.path.isfile(config):
        return True

    for line in fileinput.FileInput(config, inplace=True):
        for find, replace in replacements.items():
            line = line.replace(find, replace)

        print(line, end=' ')
