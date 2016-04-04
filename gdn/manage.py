from flask.ext.script import Manager
from . import app
import loader

manager = Manager(app)

deprecation = '''
This command has been deprecated! Please use uwsgi instead! Example:

    uwsgi -s /tmp/uwsgi.sock -w gdn:app

For more info on production use, see: http://uwsgi-docs.readthedocs.org/en/latest/Nginx.html
If you do not intend to use this in production, use the "debug" command instead!
'''


@manager.command
def run():
    print(deprecation)


@manager.command
def debug():
    app.run(debug=app.config['DEBUG'], host=app.config['HTTP_HOST'],
            port=app.config['HTTP_PORT'])


@manager.command
def load(only=None):
    try:
        loader.run(app.config, only)
    except KeyboardInterrupt:
        return
