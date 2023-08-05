import configparser
from sqlalchemy import create_engine, MetaData, Table


engine = create_engine('sqlite:///census.sqlite')
connection = engine.connect()
metadata = MetaData()
census = Table('census', metadata, autoload=True, autoload_with=engine)

config = configparser.ConfigParser()
config.read('config.txt')

engine = engine = create_engine('sqlite:///:memory:', echo=True)
create_engine(config.get('database', 'con'))