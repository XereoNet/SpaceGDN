import os

_path = os.path.dirname(os.path.realpath(__file__))

def loadSources():

	import glob, json

	files = glob.glob(_path + '/../sources/*.json')
	output = {}

	for f in files:

		with open(f) as handle:
			contents = json.load(handle)

		output[ contents['name'] ] = contents

	return output

def load():
	sources = loadSources()

	for source in sources.iteritems():
		#print 'Loading source ' + source['name']
		print 'Loading'