from flask import Flask, render_template
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config.from_pyfile('../config.py')

if app.config['RAVEN_DSN']:
    sentry = Sentry(app, dsn=app.config['RAVEN_DSN'])

@app.route('/')
def index():
    return render_template('index.html')
