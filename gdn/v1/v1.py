from flask import Blueprint, render_template, request
from gdn.v1 import response
from gdn.util import request_wants_json

mod = Blueprint('v1', __name__, url_prefix='/v1', template_folder='templates',
                static_folder='static')


@mod.route('/<path:path>')
def resolve(path):

    res = response.run(path)

    if request_wants_json() or 'json' in request.args:
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    else:
        return render_template('json.html', path='/v1/' + path,
                               method=request.method, data=res)
