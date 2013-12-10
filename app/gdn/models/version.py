from gdn import db

class Version(db.Model):
	__tablename__ = 'versions'

	id = db.Column(db.Integer, primary_key = True)
	channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
	version = db.Column(db.String(32))
	updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.utc_timestamp())

	channel = db.relationship("Channel", backref = "versions")
	__table_args__ = (db.UniqueConstraint('channel_id', 'version', name='uix_1'), )