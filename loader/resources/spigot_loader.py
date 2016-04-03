import requests
import json
import re
import datetime
import os
import glob
from xml.etree import ElementTree
from ..resource_bases import Jenkins


class Spigot(Jenkins):

    def items(self):
        with open(os.path.join(os.path.dirname(__file__), "jenkins/spigot.json")) as f:
            desc = json.load(f)
            for item in self.type_items(desc):
                yield item

    def get_versions(self, desc, build):
        if not "lastBuiltRevision" in build["actions"][2]:
            return None, None
        commit = build["actions"][2]["lastBuiltRevision"]["SHA1"]
        patch_url = desc["patch_url_format"].format(commit)
        patch_content = requests.get(patch_url).text
        version = re.search(desc["version_regexp"], patch_content, re.MULTILINE)
        if version is None:
            return None, None
        version = version.group(1)
        return version, re.search(desc["game_version_regexp"], version).group(1)
