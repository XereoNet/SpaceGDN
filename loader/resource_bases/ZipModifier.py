import zipfile
import os
import tempfile
import shutil
import requests

from distutils import dir_util
from ..util import get_download_path, md5sum_text


class ZipModifier:

    def __init__(self):
        self.temp_dir_path = None
        self.file_path = None
        self.type = None

    def download(self, url, file):
        r = requests.get(url, stream=True)
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def start_from_remote(self, url):
        _, temp_file_path = tempfile.mkstemp()
        self.download(url, temp_file_path)
        self.temp_dir_path = tempfile.mkdtemp()

        self.unzip(temp_file_path, self.temp_dir_path)
        os.remove(temp_file_path)

    def start_from_local(self, local_filename):
        file_path = local_filename
        _, temp_file_path = tempfile.mkstemp()
        self.temp_dir_path = tempfile.mkdtemp()

        shutil.move(file_path, temp_file_path)
        self.unzip(temp_file_path, self.temp_dir_path)
        os.remove(temp_file_path)

    def end_modify(self, destination):
        self.zip(self.temp_dir_path, destination)
        shutil.rmtree(self.temp_dir_path)

    def unzip(self, source_filename, dest_dir):
        with zipfile.ZipFile(source_filename) as z:
            z.extractall(dest_dir)

    def zip(self, source_dir, dest_filename):
        name, ext = os.path.splitext(dest_filename)
        shutil.make_archive(name, ext[1:], source_dir, '.')

    def ensure_dir_present(self, directory):
        if isinstance(directory, str):
            path = os.path.join(self.temp_dir_path, directory)
            if not os.path.exists(path):
                os.makedirs(path)
                open(os.path.join(path, '.keep'), 'a').close()
        else:
            for d in directory:
                self.ensure_dir_present(d)

    def ensure_dir_absent(self, directory):
        path = os.path.join(self.temp_dir_path, directory)
        shutil.rmtree(path)

    def ensure_file_present(self, filename):
        path = os.path.join(self.temp_dir_path, filename)
        if not os.path.isfile(path):
            open(os.path.join(path), 'a').close()

    def ensure_file_absent(self, filename):
        path = os.path.join(self.temp_dir_path, filename)
        os.remove(path)

    def replace_in_file(self, filename, replacements):
        path = os.path.join(self.temp_dir_path, filename)
        if not os.path.isfile(path):
            return True

        _, outpath = tempfile.mkstemp()
        with open(outpath, 'w') as outfile:
            with open(path) as infile:
                for line in infile:
                    for needle, replace in replacements.items():
                        line = line.replace(needle, replace)

                    outfile.write(line)

        os.remove(path)
        os.rename(outpath, path)

    def patch_from_local(self, source, target=''):
        path = os.path.join(self.temp_dir_path, target)
        dir_util.copy_tree(source, path)

    def patch_from_remote(self, url, target='', force=False):
        dlpath = get_download_path('patch_' + md5sum_text(url))

        if force or not os.path.exists(dlpath):
            _, temp_file_path = tempfile.mkstemp()
            self.download(url, temp_file_path)


            with zipfile.ZipFile(temp_file_path) as z:
                z.extractall(dlpath)

            os.remove(temp_file_path)

        return self.patch_from_local(dlpath, target)