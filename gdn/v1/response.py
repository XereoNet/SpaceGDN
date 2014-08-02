from flask import json, make_response, request
from gdn.v1 import lang, builder, handler
from gdn import app

from gdn.models import * 
from datetime import datetime

def show_error(code, tup = ()):
    error = {
        'success': False,
        'error': {
            'code': code,
            'message': lang.errors[code] % tup
        },
        'results': [],
        'pages': {}
    }
    return make_response((json.dumps(error), 400))

def check_ip(ip):
    if not app.config['RATE_LIMIT']:
        return True

	record = API_Request.query.filter(API_Request.ip == ip).first()

	if not record:
		record = API_Request()
		record.ip = ip
		record.requests = 0
		record.updated_at = datetime.now()
		db.session.add(record)

	delta = datetime.now() - record.updated_at

	if delta.total_seconds() > 3600:
		record.requests = 0
		record.updated_at = datetime.now()

	record.requests += 1
	db.session.commit()

	if record.requests > 1000:
		return False
	else:
		return True

def run(path):

	if not check_ip(request.remote_addr):
		return show_error(492)

	parts = path.rstrip('/').split('/')

	try:
		data = builder.build(parts)
		pager = handler.handle_query(data)
	except Exception as e:
		return show_error(e.args[0], e.args[1])

	reponse = {
		'success': True,
		'error': {},
		'results': handler.to_dict(pager.items),
		'pages': {
			'pages': pager.pages,
			'has_next': pager.has_next,
			'has_prev': pager.has_prev,
			'current_page': pager.page,
			'total_items': pager.total
		}
	}

	res = make_response((json.dumps(reponse), 200))
	return res