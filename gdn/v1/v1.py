from flask import Blueprint, render_template
from gdn.v1 import response, builder

mod = Blueprint('v1', __name__, url_prefix='/v1')

@mod.route('/', defaults={'path': ''})
def index(path):
	return render_template('index.html')

@mod.route('/<path:path>')
def resolve(path):

	parts = path.split('/')
	data = builder.build(parts)

	return response.run(data)