import os
import os.path
import tempfile
import requests
import subprocess
from ..util import get_download_path
from distutils.version import LooseVersion
from bs4 import BeautifulSoup
from . import ZipModifier
from gdn.log import logger

class ForgePatcher(ZipModifier):

    url_format = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/index_{}.html"
    download_format = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/{0}/forge-{0}-installer.jar"

    def patch_download(self, mc_version, url, path, md5sum=None):
        logger.info("Patching from URL " + url)
        self.start_from_remote(url, md5sum)
        self.move_from_subdirectory("minecraft")
        self.patch_from_local(self.get_patch(mc_version))
        self.end_modify(path)

    def get_patch(self, mc_version):
        if LooseVersion(mc_version) < LooseVersion("1.6.1"):
            raise Exception("Patching is not implemented for Minecraft < 1.6.1")
        logger.info("Finding patch for " + mc_version)
        patch_path = get_download_path("forge_patch-" + mc_version)

        if not os.path.isdir(patch_path):
            logger.info("   Patch not found, creating")
            os.mkdir(patch_path)
            forge_url = self.get_forge(mc_version)
            jar_path = os.path.join(patch_path, "forge-install.jar")
            self.download(forge_url, jar_path)

            subprocess.check_call(["java", "-jar", "forge-install.jar", "--installServer"],
                                  stdout=subprocess.DEVNULL, cwd=patch_path)
            os.remove(jar_path)
            if os.path.isfile(jar_path + ".log"):
                os.remove(jar_path + ".log")
        else:
            logger.info("    Had patch from before")

        return patch_path


    def get_forge(self, mc_version):
        url = self.url_format.format(mc_version)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        version_string = soup.find("div", {"class": "download"}).find("small").get_text()
        version_string = version_string.replace(" ", "")

        # Forge fucked up with the naming of this version, for some reason...
        if version_string.startswith("1.7.10"):
            version_string = version_string + "-1.7.10"

        return self.download_format.format(version_string)
