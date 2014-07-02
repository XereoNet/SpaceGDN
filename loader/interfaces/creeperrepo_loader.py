import requests, urllib, re
from lxml import etree as ET

class loader_creeperrepo:

	base_url = 'http://www.creeperrepo.net'

	def artifactURL(self, name):
		return self.base_url + '/FTB2/static/modpacks.xml'

	def getData(self, name, version, file_):

		url = self.base_url + '/FTB2/' + urllib.quote_plus('modpacks^'+name+'^'+version+'^'+file_)

		# site = requests.head(url)

		# size = site.headers['content-length'];

		return url

	def getXML(self, name):
		r = requests.get(self.artifactURL(self))

		return ET.fromstring(r.content).find('modpack[@name="%s"]' % name)

	def load(self, channel, last_build):
		modpack = self.getXML(channel['full_name'])

		build = re.sub('[^0-9]', '', modpack.get('repoVersion'))
		if build == last_build:
			return []

		version = modpack.get('version')

		url = self.getData(modpack.get('dir'), re.sub('\.', '_', modpack.get('repoVersion')), modpack.get('serverPack'))

		return [{
			'version': modpack.get('version'),
			'size': None,
			'checksum': None,
			'url': url,
			'build': build
		}]