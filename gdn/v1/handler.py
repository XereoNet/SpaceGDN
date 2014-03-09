import sys
from gdn import app
from flask import request

from sqlalchemy.util import KeyedTuple
from gdn.models import * 

def getModel(name):
    return getattr(sys.modules[__name__], name.capitalize())

def joinerQuery(query, pointer):
    clutch_in = True
    for part in reversed(app.config['HEIRARCHY']):
        if clutch_in == False:
            model = getModel(part['name'])
            query = query.join(model).add_columns(model.id.label(part['name'] + '_id'))
        if part['name'] == pointer:
            clutch_in = False

    return query

def applySorting(query, params):
    if not 'sort' in params:
        return query

    splits = params['sort'].lower().split('.')
    if not len(splits) == 3:
        return query

    [model_name, column, direction] = splits

    if not direction == 'asc' and not direction == 'desc':
        return query
    if not model_name in [m['name'] for m in app.config['HEIRARCHY']]:
        return query

    model = getModel(model_name)

    if not column in model.__table__.columns:
        return query

    m_columns = getattr(model, column)
    m_direction = getattr(m_columns, direction)

    return query.order_by(m_direction())

def to_dict(ls):
    out = []
    for result in ls:
        if isinstance(result, KeyedTuple):
            model = result[0]
        else:
            model = result
            result = []
        data = {}
        data['id'] = getattr(model, 'id')
     
        for col in model._sa_class_manager.mapper.mapped_table.columns:
            data[col.name] = getattr(model, col.name)

        l = len(result)

        for index in range(1, l):
            data[app.config['HEIRARCHY'][l - index - 1]['name'] + '_id'] = result[index]

        out.append(data)
 
    return out

def getNum(num, default = 0):
    try: 
        return int(num)
    except Exception:
        return default

def handle_query(data):
    query = getModel(data['select']).query
    query = joinerQuery(query, data['select'])
    query = applySorting(query, request.args)

    for key, value in data['data'].iteritems():
        model = getModel(key)
        query = query.filter(getattr(model, 'id') == value)

    page = getNum(request.args.get('page'), 1)

    return query.paginate(page, 100, False)