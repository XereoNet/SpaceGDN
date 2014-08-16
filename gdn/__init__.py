from .app import app
from .manage import manager
from .mongo import db
from .v2 import blueprint

app.register_blueprint(blueprint)