from sqlalchemy import create_engine
from .. import config
connection_string = config.database['engine'] + '://' + config.database['username'] + ':' + config.database['password'] + '@' + config.database['host'] + '/' + config.database['db']
engine = create_engine(connection_string)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()