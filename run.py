#!/bin/python
from app import app, config
app.run(debug = True, host=config.http['host'], port=config.http['port'])
