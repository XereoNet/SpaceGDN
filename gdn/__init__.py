from flask import Flask

app = Flask(__name__)

from gdn.v1 import v1
app.register_blueprint(v1.mod)