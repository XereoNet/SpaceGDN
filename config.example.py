# App settings
DEBUG = True
TESTING = True
SECRET_KEY = "SUPERSECRET"
# Whether to always cache servers. This has no effect if CACHE_PATCHED is False
CACHE_ALWAYS = False
# Whether to only cache patched(servers with a Modifier) servers.
CACHE_PATCHED = True
# Never download servers. This overrides both CACHE_ properties
NEVER_DOWNLOAD = False

# Webserver Settings
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 80

# Monog connection URI
MONGO_URI = 'mongodb://localhost:27017/'
# Mongo database name to use
MONGO_DB = 'gdn'

# Whether the API should be rate limited.
RATE_LIMIT = True

# Number of records to return per page on request
PAGE_LENGTH = 100

# Raven DSN. If False, Raven handler will not be enabled.
RAVEN_DSN = False
