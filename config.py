# App settings
DEBUG = True
TESTING = True
SECRET_KEY = "SUPERSECRET"

# Database settings
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@127.0.0.1/spacegdn'
SQLALCHEMY_ECHO = True

# Webserver Settings
HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8000