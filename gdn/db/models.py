from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from .. import config

import connection

class Build(connection.Base):
	__tablename__ = 'builds'

	id = Column(Integer, primary_key = True)
	version_id = Column(Integer, ForeignKey('versions.id'))
	build = Column(Integer)
	downloads = Column(Integer)
	size = Column(Integer)
	checksum = Column(String(32))
	url = Column(String(150))
	created_at = Column(DateTime, default = datetime.now)

	version = relationship("Version", backref = "builds")

class Version(connection.Base):
	__tablename__ = 'versions'

	id = Column(Integer, primary_key = True)
	channel_id = Column(Integer, ForeignKey('channels.id'))
	version = Column(String(32))
	updated_at = Column(DateTime, default = datetime.now)

	channel = relationship("Channel", backref = "versions")

class Channel(connection.Base):
	__tablename__ = 'channels'

	id = Column(Integer, primary_key = True)
	jar_id = Column(Integer, ForeignKey('jars.id'))
	name = Column(String(32))
	updated_at = Column(DateTime, default = datetime.now)

	jar = relationship("Jar", backref = "channels")

class Jar(connection.Base):
	__tablename__ = 'jars'

	id = Column(Integer, primary_key = True)
	name = Column(String(32))
	site_url = Column(String(100))
	updated_at = Column(DateTime, default = datetime.now)

def migrate():
	connection.Base.metadata.drop_all(connection.engine)

	connection.Base.metadata.create_all(connection.engine)

	connection.session.commit()