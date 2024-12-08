from config import database_url
from sqlalchemy import create_engine, Column, TIMESTAMP, BIGINT, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

''' Script for setting up the database schema and tables '''

## Define the base model for SQLAlchemy ORM
Base = declarative_base()

class Characters(Base):
    """
    ORM model for the 'characters' table.
    """
    __tablename__ = 'characters'
    character_id = Column(BIGINT , primary_key=True)
    name = Column(Text, index=True)
    description = Column(Text)
    thumbnail = Column(Text)
    modified = Column(TIMESTAMP)

class Comics(Base):
    """
    ORM model for the 'comics' table.
    """
    __tablename__ = 'comics'
    character_id = Column(BIGINT, primary_key=True)
    comic_name = Column(Text, index=True)
    comic_resourceURI = Column(Text)

class Events(Base):
    """
    ORM model for the 'events' table.
    """
    __tablename__ = 'events'
    character_id = Column(BIGINT, primary_key=True)
    event_name = Column(Text, index=True)
    event_resourceURI = Column(Text)

class Series(Base):
    """
    ORM model for the 'series' table.
    """
    __tablename__ = 'series'
    character_id = Column(BIGINT, primary_key=True)
    series_name = Column(Text, index=True)
    series_resourceURI = Column(Text)

class Stories(Base):
    """
    ORM model for the 'stories' table.
    """
    __tablename__ = 'stories'
    character_id = Column(BIGINT, primary_key=True)
    story_name = Column(Text, index=True)
    story_type = Column(Text)
    story_resourceURI = Column(Text)


## Create database engine
engine = create_engine(database_url)

## Check if the database exists, and create it if it doesn't
if not database_exists(engine.url):
    create_database(engine.url)

## Create tables in the database based on the defined models
Base.metadata.create_all(engine)

## Add an entry point for standalone execution
if __name__ == "__main__":
    print("Creating tables in the database...")
    Base.metadata.create_all(engine)
    print("Tables created successfully.")