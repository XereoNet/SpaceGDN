from flask import Blueprint, render_template, jsonify
from gdn.v1 import response, builder

mod = Blueprint('v1', __name__, url_prefix='/v1')

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

	return jsonify(response.run(data))