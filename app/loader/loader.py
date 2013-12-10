import os, yggdrasil
from interfaces import *
from gdn import app

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
	return channel.query\
		.filter(channel.name == data['name'])\
		.join(version, version.channel_id == channel.id)\
		.join(build, build.version_id == version.id)\
		.add_columns(build.build, build.created_at, channel.name)\
		.order_by(build.build.desc())\
		.first()

def getAndMake(filters, model, data, ignore = []):
	item = connection.session.query(model).filter_by(**filters).first()
	if not item:
		item = model(**data)
		session.add(item)
	else:
		for key, value in data.iteritems():
			if not key in ignore:
				setattr(item, key, value)
	return item

def getLoader(name):
	if not 'loader_' + name in globals():
		app.logger.warning('Interface not found, "%s"' % name)
		return False

	return globals()['loader_' + name]()

def load():
	sources = loadSources()

	adder = yggdrasil.Yggdrasil()

	for source in sources:

		jar_obj = adder.addJar(source)

		for channel_data in source['channels']:
			channel = adder.addChannel(channel_data, jar_obj)
			l = getLoader(channel_data['interface'])

			if not l: continue;

			for build in l.load(channel_data):
				adder.addBuild(build, channel)

	adder.commit()