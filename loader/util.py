import os
import hashlib


def get_download_path(filename):
    return os.path.join('gdn/static/cache', filename)


def md5sum_text(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()
