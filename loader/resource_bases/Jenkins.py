import requests
import json
import re
import datetime
import os
import glob
from xml.etree import ElementTree
from . import Downloader


class Jenkins(Downloader):

    def items(self):
        ''' Load all items from all maven jenkins sources '''
        jsons = glob.glob(os.path.join(os.path.dirname(__file__),
                          "../resources/jenkins/*.maven.json"))

        for j in jsons:
            with open(j) as f:
                desc = json.load(f)
                for item in self.type_items(desc):
                    yield item

    def type_items(self, desc):
        ''' Load all items from a maven jenkins source '''
        data = self.call_jenkins(desc['jenkins_url'])

        if data is None:
            return

        builds = data["builds"][:desc["limit"]]
        for build in desc["special_builds"]:
            builds.append({
                "number": build,
                "url": desc["jenkins_url"] + str(build) + "/"
            })

        for build in builds:
            details = self.call_jenkins(build['url'])
            if details is None:
                continue
            version, game_version = self.get_versions(desc, details)
            if version is None:
                continue
            url = self.get_url(details)

            yield {
                "$parents": [
                    {
                        "$id": desc["game_id"],
                        "resource": "game",
                        "name": desc["game_name"]
                    }, {
                        "$id": desc["id"],
                        "resource": "type",
                        "name": desc["name"],
                        "description": desc["description"],
                        "author": desc["author"]
                    }, {
                        "$id": version,
                        "resource": "version",
                        "version": version,
                        "game_version": game_version,
                        "latest_build": build["number"]
                    }
                ],
                "$id": str(build["number"]),
                "$patched": False,
                "$load": lambda path: self.download(url, path),
                "resource": "build",
                "build": build["number"],
                "created": datetime.datetime.fromtimestamp(details["timestamp"]/1000),
                "url": url
            }

    def get_url(self, build):
        return build["url"] + "artifact/" + build["artifacts"][0]["relativePath"]

    def call_jenkins(self, url):
        if not url.endswith("/"):
            url += "/"
        url += "api/json"
        try:
            response = requests.get(url)
            if response.ok:
                return response.json()
        except Exception:
            return None
