from gdn import db
from datetime import datetime

class Jar(db.Model):
	__tablename__ = 'jars'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(32), unique=True)
	site_url = db.Column(db.String(100))
	updated_at = db.Column(db.DateTime, default = datetime.now)