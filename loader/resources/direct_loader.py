import json
import datetime
import os
import glob
from ..resource_bases import Downloader


class Direct(Downloader):

    def items(self):
        jsons = glob.glob(os.path.join(os.path.dirname(__file__), 'directs/*.json'))
        out = []

        for j in jsons:
            with open(j) as f:
                sources = json.load(f)

            for source in sources:
                source['$load'] = lambda path, url=source['url']: self.download(url, path)
                source['$patched'] = False
                source['created'] = datetime.datetime.fromtimestamp(source['created'])
                out.append(source)

        return out