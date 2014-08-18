import logging
import logging.handlers
import os.path
from raven.handlers.logging import SentryHandler

from .app import app

formatter = logging.Formatter(app.config['LOG_FORMAT'])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.handlers.RotatingFileHandler(os.path.join(os.path.dirname(__file__), '../gdn.log'),
                                          maxBytes=app.config['LOG_ROTATION_SIZE'],
                                          backupCount=app.config['LOG_ROTATION_BACKUP'])
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

if app.config['RAVEN_DSN']:
    sh = SentryHandler(app.config['RAVEN_DSN'])
    sh.setLevel(app.config['RAVEN_LEVEL'])
    logger.addHandler(sh)