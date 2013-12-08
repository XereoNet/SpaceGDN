from flask import Blueprint, render_template, json, request
from flask.ext.sqlalchemy import SQLAlchemy
from gdn.v1 import response, builder
from gdn.util import request_wants_json

mod = Blueprint('v1', __name__, url_prefix='/v1', template_folder='templates',  static_folder='static')

def to_json(ls):
	out = []
	for model in ls:
		data = {}
		data['id'] = getattr(model, 'id')
	 
		for col in model._sa_class_manager.mapper.mapped_table.columns:
			data[col.name] = getattr(model, col.name)
		out.append(data)
 
	return json.dumps(out)

@mod.route('/', defaults={'path': ''})
def index(path):
	return render_template('index.html')

@mod.route('/<path:path>')
def resolve(path):

	parts = path.split('/')
	try:
		data = builder.build(parts)
	except Exception as e:
		return e.args[0], 400

	result = response.run(data)

	data = to_json(result)
	print data
	if (request_wants_json()):
		return data
	else:
		return render_template('json.html',
			path = request.url,
			method = request.method,
			data = data
		)