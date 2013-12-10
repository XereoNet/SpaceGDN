from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from models import *

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
	app.run(debug = app.config['DEBUG'], host=app.config['HTTP_HOST'], port=app.config['HTTP_PORT'])

manager.run()

from gdn.v1 import v1
app.register_blueprint(v1.mod)