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
	IOLoop.instance().start()

def debug():
	app.run(debug = app.config['DEBUG'], host=app.config['HTTP_HOST'], port=app.config['HTTP_PORT'])

@manager.command
def load():
	from loader import loader
	loader.load()