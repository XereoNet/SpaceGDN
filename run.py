#!env/bin/python
from gdn import app, config
app.run(debug = True, host=config.http['host'], port=config.http['port'])
