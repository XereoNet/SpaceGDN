#!flask/bin/python
from gdn.db import models
print 'Starting migrations...'
models.migrate()
print 'Ok!'