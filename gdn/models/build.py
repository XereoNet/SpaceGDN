from gdn import db

class Build(db.Model):
	__tablename__ = 'builds'

	id = db.Column(db.Integer, primary_key = True)
	version_id = db.Column(db.Integer, db.ForeignKey('versions.id'), nullable=False)
	build = db.Column(db.Integer, nullable=False)
	size = db.Column(db.Integer, nullable=True)
	checksum = db.Column(db.String(32), nullable=True)
	url = db.Column(db.String(150), nullable=False)
	created_at = db.Column(db.TIMESTAMP, nullable=False)
	updated_at = db.Column(db.TIMESTAMP, nullable=False)

	version = db.relationship("Version", backref = "builds")
	__table_args__ = (db.UniqueConstraint('version_id', 'build', name='uix_1'), )