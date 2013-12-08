from flask import Blueprint, render_template, request
from gdn.v1 import response, builder
from gdn.util import request_wants_json

mod = Blueprint('v1', __name__, url_prefix='/v1', template_folder='templates',  static_folder='static')

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

	res = response.run(data)

	if (request_wants_json()):
		return res
	else:
		return render_template('json.html',
			path = request.url,
			method = request.method,
			data = res
		)