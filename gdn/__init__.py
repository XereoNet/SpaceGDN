from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('../config.py')

if app.config['RAVEN_DSN']:
    from raven.contrib.flask import Sentry
    sentry = Sentry(app, dsn=app.config['RAVEN_DSN'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from gdn.v1 import v1
app.register_blueprint(v1.mod)


@app.route('/', defaults={'path': ''})
def index(path):
    return render_template('index.html')

from gdn.manage import manager
