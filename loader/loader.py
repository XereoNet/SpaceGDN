import os, importlib

from gdn.db import connection, models

_path = os.path.dirname(os.path.realpath(__file__))

def loadSources():

	import glob, json

	files = glob.glob(_path + '/../sources/*.json')
	output = []

	for f in files:

		with open(f) as handle:
			output.append(json.load(handle))

	return output

def getLastBuild(data):
	return connection.session.query(models.Channel)\
		.filter(models.Channel.name == data['name'])\
		.join(models.Version, models.Version.channel_id == models.Channel.id)\
		.join(models.Build, models.Build.version_id == models.Version.id)\
		.order_by(models.Build.build.desc())\
		.first()

def load():
	sources = loadSources()

	for source in sources:
		print 'Loading source "%s"' % source['name']

		for channel in source['channels']:
			module = importlib.import_module('loader', channel['interface'])

			last = getLastBuild(channel)