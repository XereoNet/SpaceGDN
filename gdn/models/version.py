from gdn import db
from datetime import datetime

class Version(db.Model):
	__tablename__ = 'versions'

	id = db.Column(db.Integer, primary_key = True)
	channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
	version = db.Column(db.String(32))
	updated_at = db.Column(db.DateTime, default = datetime.now)

	channel = db.relationship("Channel", backref = "versions")
	__table_args__ = (db.UniqueConstraint('channel_id', 'version', name='uix_1'), )