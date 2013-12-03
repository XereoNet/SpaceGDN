from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)

from gdn.v1 import v1
app.register_blueprint(v1.mod)