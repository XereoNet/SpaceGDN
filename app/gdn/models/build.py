from gdn import db
from datetime import datetime

class Build(db.Model):
	__tablename__ = 'builds'

	id = db.Column(db.Integer, primary_key = True)
	version_id = db.Column(db.Integer, db.ForeignKey('versions.id'))
	build = db.Column(db.Integer)
	downloads = db.Column(db.Integer)
	size = db.Column(db.Integer)
	checksum = db.Column(db.String(32))
	url = db.Column(db.String(150))
	created_at = db.Column(db.DateTime, default = datetime.now)

	version = db.relationship("Version", backref = "builds")
	__table_args__ = (db.UniqueConstraint('version_id', 'build', name='uix_1'), )