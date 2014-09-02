from flask import Blueprint, request, abort, json
from multiprocessing import Pool
from ..app import app
from .status import status
import loader

blueprint = Blueprint('private', __name__)


@blueprint.before_request
def require_key():
    if not 'PRIVATE_KEY' in app.config:
        return abort(400)

    if app.config['PRIVATE_KEY'] != request.args.get('key'):
        return abort(403)

@blueprint.route('/status')
def show_status():
    return json.dumps({'success': True, 'status': status.get()}), 200

@blueprint.route('/update')
def update():
    if status.get() != 'idle':
        return json.dumps({'success': False, 'error': 'GDN is already busy!'})

    pool = Pool(processes=1)
    pool.apply_async(loader.run, [app.config], lambda: status.set('idle'))
    status.set('loading')

    return show_status()