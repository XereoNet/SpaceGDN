from gdn import db

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key = True)
    jar_id = db.Column(db.Integer, db.ForeignKey('jars.id'), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)

    jar = db.relationship("Jar", backref = "channels")
    __table_args__ = (db.UniqueConstraint('jar_id', 'name', name='uix_1'), )