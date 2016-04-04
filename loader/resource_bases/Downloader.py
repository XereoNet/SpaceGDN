import hashlib
import requests
from gdn.log import logger

class Downloader():
    def download(self, url, file, md5sum=None, is_retry=False, expect=None):
        r = requests.get(url, stream=True)
        if not r.ok:
            raise Exception("Not OK response from: " + url)
        if not expect is None and not expect in r.headers["content-type"]:
            raise Exception("Not expected content-type, '{}'! Got: '{}'".format(expect, r.headers["content-type"]))
        md5 = hashlib.md5()
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    md5.update(chunk)
                    f.flush()

        digest = md5.hexdigest()
        if not md5sum is None and md5sum != digest:
            if not is_retry:
                logger.info('Retrying download of %s, md5sum %s did not match expected %s' % (url, digest, md5sum))
                self.download(url, file, md5sum, True)
            else:
                logger.warn('Retried download, still did not checksum correctly. Continuing anyway')
