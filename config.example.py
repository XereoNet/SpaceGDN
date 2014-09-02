import logging

# App settings. Debug and testing should be set to "False" in production, and
# the secret key should be randomized. It's not used *yet*, but it may be in
# the future.
DEBUG = True
TESTING = True
SECRET_KEY = "SUPERSECRET"
# Whether to always cache servers. This has no effect if CACHE_PATCHED is False.
CACHE_ALWAYS = False
# Whether to only cache patched(servers with a Modifier) servers.
CACHE_PATCHED = True

# Webserver Settings
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 80

# Monog connection URI
MONGO_URI = 'mongodb://localhost:27017/'
# Mongo database name to use
MONGO_DB = 'gdn'

# Rate limit tuple in the format <number of requests>, <minutes interval>.
# Or, False if you do not want any rate limiting.
RATE_LIMIT = 1000, 60

# Number of seconds to keep usage records for.
KEEP_USAGE_FOR = 60 * 60 * 24 * 7

# The "key" needed to access private routes. This should be passed as a GET or
# POST parameter. Uncomment it to enable the private key and private routes.
# PRIVATE_KEY = 'verySeekrit'

# Whether IP/agent stats should be collected and displayed publicly.
COLLECT_STATS = True

# Number of records to return per page on request
PAGE_LENGTH = 100

# Raven DSN. If False, Raven handler will not be enabled. See getsentry.com
# if you would like to use this. It's fantasic!
RAVEN_DSN = False
# Level of error message which will be logged to Raven
RAVEN_LEVEL = logging.WARN

# Level of events which should be logged to the log/gdn.log file.
LOG_LEVEL = logging.INFO
# How large the log should get before being rotated. Default: 100 MB
LOG_ROTATION_SIZE = 2 << 20
# Number of log rotations to keep
LOG_ROTATION_BACKUP = 5
# Format of the console and file log
LOG_FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'