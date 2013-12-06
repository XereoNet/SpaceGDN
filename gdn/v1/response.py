import sys

from gdn import app
from gdn.models import * 

def getModel(name):
	return getattr(sys.modules[__name__], name.capitalize())

def joinerQuery(query, pointer):
	clutch_in = True
	previous_name = ''
	for part in app.config['HEIRARCHY']:
		if clutch_in == False:
			model = getModel(part['name'])
			query = query.join(model, getattr(model, previous_name + '_id') == model.id)
		elif part['name'] == pointer:
			clutch_in = False
		previous_name = part['name']

	return query

def run(data):

	query = getModel(data['select']).query
	joinerQuery(query, data['select'])

	for key, value in data['data'].iteritems():
		model = getModel(key)
		query = query.filter(getattr(model, 'id') == value)

	return query.all()