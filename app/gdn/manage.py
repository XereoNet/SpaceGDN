from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

from models import *
from . import app

manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
	from tornado.wsgi import WSGIContainer
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop

	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(app.config['HTTP_PORT'])
	try:
		print '''===========================================================================
   __...____________________          ,
   `(\ [ ===SPACEGDN===--|__|) ___..--"_`--.._____
     `"""""""""""""""""| |""` [_""_-___________"_/
                       | |   /..../`'-._.-'`
                   ____| |__/::..'_
                  |\ ".`"` '_____//\\
                  `"'-.   """""  \\\\/
                       `""""""""""`
===========================================================================
SpaceGDN developed by pyxld.com and is OSS under the MPL-2.0 at
https://github.com/connor4312/SpaceGDN. We're lifting off...
==========================================================================='''
		IOLoop.instance().start()
	except KeyboardInterrupt:
		print '''
SpaceGDN has shut down. Find any bugs? Report on our Github project above.
===========================================================================
'''
		IOLoop.instance().stop()

@manager.command
def debug():
	app.run(debug = app.config['DEBUG'], host=app.config['HTTP_HOST'], port=app.config['HTTP_PORT'])

@manager.command
def load():
	from loader import loader
	loader.load()