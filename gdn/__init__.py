from .app import app
from .manage import manager
from .mongo import db

from .v2 import blueprint as v2Blueprint
from .private import blueprint as privateBlueprint

app.register_blueprint(v2Blueprint)
app.register_blueprint(privateBlueprint)