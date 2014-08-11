from interfaces import *
from gdn import app
from gdn.models import Version, Build
import os
import yggdrasil
import sys
import traceback
import glob
import json

_path = os.path.dirname(os.path.realpath(__file__))


def loadSources():

    files = glob.glob(_path + '/../sources/*.json')
    output = []

    for f in files:
        with open(f) as handle:
            output.append(json.load(handle))

    return output


def getLastBuild(channel_id):
    return Version.query\
        .filter(Version.channel_id == channel_id)\
        .join(Build, Build.version_id == Version.id)\
        .add_columns(Build.build)\
        .order_by(Build.build.desc())\
        .first()


def getAndMake(filters, model, data, ignore=[]):
    item = connection.session.query(model).filter_by(**filters).first()
    if not item:
        item = model(**data)
        session.add(item)
    else:
        for key, value in data.iteritems():
            if key not in ignore:
                setattr(item, key, value)
    return item


def getLoader(name):
    if not 'loader_' + name in globals():
        app.logger.warning('Interface not found, "{}"'.format(name))
        return False

    return globals()['loader_' + name]()


def cap(s, l):
    return s if len(s) <= l else s[0:l-3] + '...'


def load(config):
    sources = loadSources()

    adder = yggdrasil.Yggdrasil(config)

    for source in sources:
        source['description'] = cap(source['description'], 200)

        jar_obj = adder.addJar(source)

        for channel_data in source['channels']:
            channel = adder.addChannel(channel_data, jar_obj)
            l = getLoader(channel_data['interface'])

            print("\nLoading builds for {}#{}".format(source['name'],
                                                      channel_data['name']))

            if not l:
                continue

            data = getLastBuild(channel)
            last_build = 0
            if data:
                last_build = data.build

            try:
                for build in l.load(channel_data, last_build):
                    adder.addBuild(build, channel, source['name'])
            except Exception as err:
                print '=' * 75
                traceback.print_exc()
                print '=' * 75
                print 'Loading of {}#{} failed, continuing...'.format(
                    source['name'], channel_data['name'])

        adder.commit()
        sys.stdout.write("\n\n")
