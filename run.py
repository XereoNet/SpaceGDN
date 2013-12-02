#!env/bin/python

print "SpaceGDN is loading up!"
from loader import loader
loader.load()

print "Web server starting..."
from gdn import app, config

app.run(debug = True, host=config.http['host'], port=config.http['port'])
