import zipfile
import os
import tempfile
import shutil
import imp


class Modifier:

    script = None

    def __init__(self, name):
        script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'helpers/{}.py'.format(name))

        if not os.path.exists(script_path):
            return None

        self.script = self.loadFileScript(script_path)

    def modify(self, local_filename, build):
        if self.script is None:
            return False

        file_path = local_filename
        _, temp_file_path = tempfile.mkstemp()
        temp_dir_path = tempfile.mkdtemp()

        os.rename(file_path, temp_file_path)
        self.unzip(temp_file_path, temp_dir_path)
        self.script.modify(temp_dir_path, build)
        self.zip(temp_dir_path, file_path)
        shutil.rmtree(temp_dir_path)
        os.remove(temp_file_path)

        return True

    def unzip(self, source_filename, dest_dir):
        with zipfile.ZipFile(source_filename) as z:
            z.extractall(dest_dir)

    def zip(self, source_dir, dest_filename):
        name, ext = os.path.splitext(dest_filename)
        shutil.make_archive(name, ext[1:], source_dir, '.')

    def loadFileScript(self, filepath):

        mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

        if file_ext.lower() == '.py':
            return imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            return imp.load_compiled(mod_name, filepath)

        return None
