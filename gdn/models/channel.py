from gdn import db
from datetime import datetime

class Channel(db.Model):
	__tablename__ = 'channels'

	id = db.Column(db.Integer, primary_key = True)
	jar_id = db.Column(db.Integer, db.ForeignKey('jars.id'))
	name = db.Column(db.String(32))
	updated_at = db.Column(db.DateTime, default = datetime.now)

	jar = db.relationship("Jar", backref = "channels")
	__table_args__ = (db.UniqueConstraint('jar_id', 'name', name='uix_1'), )