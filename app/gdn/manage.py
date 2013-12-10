from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from models import *
from . import app, db

manager = Manager(app)

manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)

@manager.command
def run():
	app.run(debug = app.config['DEBUG'], host=app.config['HTTP_HOST'], port=app.config['HTTP_PORT'])