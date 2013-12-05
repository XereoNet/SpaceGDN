import os, importlib

from gdn.db import channel, version, build, jar

from datetime import datetime

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

def insertDataWaterfall(jars):

	heir = [{
		'name': 'jar',
		'unique': 'name'
	}, {
		'name': 'channel',
		'unique': 'name'
	}, {
		'name': 'version',
		'unique': 'version'
	}, {
		'name': 'build',
		'unique': 'build'
	}]
	pointer = 0
	def insertData(previous, current, pointer = 0):
		args = {
			'filters': {
				'name':  current['name'],
			},
			'model': globals()[current['name'].capitalize()],
			'data': current,
			'ignore': [heir[pointer + 1] + 's']
		}
		if 0 >= pointer - 1:
			args['filters'][heir[pointer - 1] + '_id'] = previous.id

		data = getAndMake(**args)

		if len(heir) > pointer + 1:
			for item in current[ heir[pointer + 1] + 's']:
				insertData(data, item, pointer + 1)

def load():
	sources = loadSources()

	jars = []

	for source in sources:
		print 'Loading source "%s"' % source['name']

		updated = False
		ins = {
			'name': source['name'],
			'site_url': source['site_url']
		}

		for channel in source['channels']:
			module = importlib.import_module('loader', channel['interface'])

			last = getLastBuild(channel)

		if updated:
			ins['updated'] = datetime.datetime.now()
		
		jars.append(ins)