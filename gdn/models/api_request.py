from gdn import db

class API_Request(db.Model):
	__tablename__ = 'requests'

	id = db.Column(db.Integer, primary_key = True)
	requests = db.Column(db.Integer)
	ip = db.Column(db.String(45))
	updated_at = db.Column(db.TIMESTAMP)

	__table_args__ = (db.UniqueConstraint('ip', name='uix_1'), )