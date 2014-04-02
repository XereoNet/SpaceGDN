from gdn import db
from gdn.models import Jar, Channel, Version, Build

from datetime import datetime
import md5
import requests

class Yggdrasil():
	jars = {}
	channels = {}
	versions = {}
	builds = {}

	def md5sumRemote(self, url):
		r = requests.get(url)
		return md5.new(r.content).hexdigest()

	def getOrMake(self, where, model, data, ignore = []):
		item = model.query.filter_by(**where).first()

		new = False
		if not item:
			new = True
			item = model()

		for key in model.__mapper__.columns:
			table, column = str(key).split('.', 1)
			if column in data and getattr(item, column) != data[column]:
				setattr(item, column, data[column])
				item.updated_at = datetime.now()
			
		if new:
			item.created_at = datetime.now()
			db.session.add(item)
			db.session.commit()

		return item

	def addJar(self, data):
		jar = self.getOrMake(model = Jar, data = data, where = {'name': data['name']})
		self.jars[jar.id] = jar

		return jar.id

	def addChannel(self, data, jar):
		if not jar in self.jars:
			raise Exception('Tried to add a channel %s in a nonexistant jar %s.' % (data['name'], jar))


		data['jar_id'] = jar
		channel = self.getOrMake(model = Channel, data = data, where = {'name': data['name'], 'jar_id': jar})
		self.channels[channel.id] = channel

		return channel.id

	def addVersion(self, version_name, channel):
		if not channel in self.channels:
			raise Exception('Tried to add a version %s in a nonexistant channel %s.' % (version_name, channel))

		data = {
			'channel_id': channel,
			'version': version_name
		}

		version = self.getOrMake(model = Version, data = data, where = data)
		self.versions[version.id] = version

		return version.id

	def addBuild(self, data, channel):
		if not channel in self.channels:
			raise Exception('Tried to add a build %s in a nonexistant channel %s.' % (data['build'], channel))
		if not data['version'] in self.versions:
			version = self.addVersion(data['version'], channel)
		else:
			version = self.versions[data['version']]

		del data['version']
		data['version_id'] = version

		if not 'checksum' in data or not data['checksum']:
			data['checksum'] = self.md5sumRemote(data['url'])

		self.getOrMake(model = Build, data = data, where = { 'build': data['build'], 'version_id': data['version_id'] })
		self.bubbleUpdate(version);

	def bubbleUpdate(self, version):
		version_model = self.versions[version]
		channel_model = self.channels[version_model.channel_id]
		jar_model = self.jars[channel_model.jar_id]

		for parent in [channel_model, version_model, jar_model]:
			parent.updated_at = datetime.now()

	def commit(self):
		db.session.commit()