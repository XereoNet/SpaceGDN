import requests, re
from bs4 import BeautifulSoup

class loader_cauldron:

	base_url = 'http://files.minecraftforge.net/Cauldron/'

	def getData(self, name):
		r = requests.get(self.base_url)
		soup = BeautifulSoup(r.content)
		table = soup.find(id="promotions_table").find_all('tr')
		del table[0]

		for tag in table:
			if tag.find('td').text == name:
				serverTag = tag.find_all('td')[4].find_all('a')[5]['href']
				url = re.sub('https?:\/\/adf\.ly\/.*?\/', '', serverTag);
				version = url[66:84];
				break;

		return {'url' : url, 'version' : version}

	def load(self, channel, last_build):
		data = self.getData(channel['name'])
		builds = []

		builds.append({
			'version': data['version'],
			'size': None,
			'checksum': None,
			'url': data['url'],
			'build': 1
			})

		return builds