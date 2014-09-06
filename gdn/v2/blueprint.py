from flask import Blueprint, render_template, request, make_response
from .collector import Collector
from .serializer import dumps
from .usage import Usage
from .requestException import RequestException

blueprint = Blueprint('v2', __name__, url_prefix='/v2', template_folder='templates', static_folder='static')
usage = Usage()

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > \
           request.accept_mimetypes['text/html']

def show_pretty_response(res, path = ''):
    res.headers.add('Access-Control-Allow-Origin', '*')

    if request_wants_json() or 'json' in request.args:
        return res
    else:
        return render_template('json.html', path='/v2/' + path, method=request.method, data=res)


@blueprint.route('/usage')
def show_usage():
    res = make_response((dumps(usage.show_usage()), 200))
    
    return show_pretty_response(res, 'usage')


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/<path:path>')
def resolve(path = ''):
    if not usage.process(request):
        return 'Rate limit exceeded', 492

    collector = Collector()
    try:
        collector.collect(request, path)
        res = make_response((dumps(collector.results()), 200))
    except RequestException as r:
        res = make_response((dumps(r.args), 400))

    return show_pretty_response(res, path)