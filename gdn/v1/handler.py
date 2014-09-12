import sys
import os.path
from gdn import app
import urllib
from flask import request
from urlparse import urlparse
from os.path import splitext, basename
from sqlalchemy.util import KeyedTuple
from gdn.models import *


def getModel(name):
    return getattr(sys.modules[__name__], name.capitalize())


def joinerQuery(query, pointer):
    clutch_in = True
    for part in reversed(app.config['HEIRARCHY']):
        if clutch_in is False:
            model = getModel(part['name'])
            query = query.join(model).add_columns(model.id.label(part['name'] +
                                                                 '_id'))
        if part['name'] == pointer:
            clutch_in = False

    return query


def isValidReference(model_name, column_name):
    if model_name not in [m['name'] for m in app.config['HEIRARCHY']]:
        return False

    model = getModel(model_name)

    return column_name in model.__table__.columns


def applySorting(query, params):
    if 'sort' not in params:
        return query

    splits = params['sort'].lower().split('.', 2)
    if not len(splits) == 3:
        return query

    [model_name, column, direction] = splits

    if not direction == 'asc' and not direction == 'desc':
        return query
    if not isValidReference(model_name, column):
        return query

    model = getModel(model_name)

    m_columns = getattr(model, column)
    m_direction = getattr(m_columns, direction)

    return query.order_by(m_direction())


def applyWheres(query, params):
    if 'where' not in params:
        return query

    expressions = params['where'].lower().split('|')
    for e in expressions:
        query = applyWhereExpression(query, e)

    return query


def applyWhereExpression(query, expression):

    splits = expression.split('.', 3)

    if not len(splits) == 4:
        return query

    [model_name, column, operator, value] = splits

    if not isValidReference(model_name, column):
        return query

    model = getModel(model_name)
    m_column = getattr(model, column)

    if operator == 'in':
        return query.filter(m_column.in_(value.split(',')))
    if operator == 'lt':
        return query.filter(m_column < value)
    if operator == 'gt':
        return query.filter(m_column > value)
    if operator == 'eq':
        return query.filter(m_column == value)
    if operator == 'lteq':
        return query.filter(m_column <= value)
    if operator == 'gteq':
        return query.filter(m_column >= value)

    return query


def to_dict(ls):
    out = []
    for result in ls:
        if isinstance(result, KeyedTuple):
            model = result[0]
        else:
            model = result
            result = []
        data = {}

        if isinstance(model, Build):
            URLdisassembled = urlparse(getattr(model, 'url'))
            URLfilename, URLfile_ext = splitext(basename(URLdisassembled.path))
            if os.path.isfile('gdn/static/cache/{}Build{}{}'.format(
                              urllib.unquote_plus(URLfilename),
                              str(getattr(model, 'build')), URLfile_ext)):
                setattr(model, 'url',
                        'http://{}:{}/static/cache/{}Build{}{}'.format(
                            app.config['HTTP_HOST'],
                            str(app.config['HTTP_PORT']), URLfilename,
                            str(getattr(model, 'build')), URLfile_ext))

        data['id'] = getattr(model, 'id')

        for col in model._sa_class_manager.mapper.mapped_table.columns:
            data[col.name] = getattr(model, col.name)

        l = len(result)

        for index in range(1, l):
            key = app.config['HEIRARCHY'][l - index - 1]['name'] + '_id'
            data[key] = result[index]

        out.append(data)

    return out


def getNum(num, default=0):
    try:
        return int(num)
    except (ValueError, TypeError):
        return default


def handle_query(data):
    query = getModel(data['select']).query
    query = joinerQuery(query, data['select'])
    query = applySorting(query, request.args)
    query = applyWheres(query, request.args)

    for key, value in data['data'].iteritems():
        model = getModel(key)
        query = query.filter(getattr(model, 'id') == value)

    page = getNum(request.args.get('page'), 1)

    return query.paginate(page, 100, False)
