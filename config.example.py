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

# Database settings
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@127.0.0.1/spacegdn'
SQLALCHEMY_ECHO = False

# Webserver Settings
HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8000

# API settings
RATE_LIMIT = True
HEIRARCHY = [{
    'name': 'jar',
    'unique': 'name'
}, {
    'name': 'channel',
    'unique': 'name'
}, {
    'name': 'version',
    'unique': 'version'
}, {
    'name': 'build',
    'unique': 'build'
}]

# Raven DSN. If False, Raven handler will not be enabled.
RAVEN_DSN = False
