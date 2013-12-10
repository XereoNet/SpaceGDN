#!env/bin/python

from gdn import app
from loader import loader
loader.load()
app.run(debug = app.config['DEBUG'], host=app.config['HTTP_HOST'], port=app.config['HTTP_PORT'])
