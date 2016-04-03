import requests
import json
import re
import datetime
import os
import glob
from xml.etree import ElementTree
from ..resource_bases import Jenkins


class JenkinsMaven(Jenkins):

    def get_versions(self, desc, build):
        if not "lastBuiltRevision" in build["actions"][2]:
            return None, None
        commit = build["actions"][2]["lastBuiltRevision"]["SHA1"]
        pom_url = desc["pom_url_format"].format(commit)
        pom_content = requests.get(pom_url).content
        pom = ElementTree.fromstring(pom_content)
        version = pom.find("{http://maven.apache.org/POM/4.0.0}version").text
        return version, re.search(desc["game_version_regexp"], version).group(1)
