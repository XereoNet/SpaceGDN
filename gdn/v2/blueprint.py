from flask import Blueprint, render_template, request, make_response
from .collector import Collector
from .serializer import dumps

blueprint = Blueprint('v2', __name__, url_prefix='/v2', template_folder='templates', static_folder='static')

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > \
           request.accept_mimetypes['text/html']

@blueprint.route('/')
@blueprint.route('/<path:path>')
def resolve(path = ''):
    collector = Collector()
    collector.collect(path, request.args.to_dict(True))

    res = make_response((dumps(collector.results()), 200))
    res.headers.add('Access-Control-Allow-Origin', '*')

    if request_wants_json() or 'json' in request.args:
        return res
    else:
        return render_template('json.html', path='/v2/' + path, method=request.method, data=res)