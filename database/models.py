from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text
)

Base = declarative_base()

def db_connect():
    return create_engine('postgresql://movies:movies@localhost/movies')

def create_table(engine):
    Base.metadata.create_all(engine)

class Movie(Base):
  __tablename__ = 'movie'

  id = Column(Integer, primary_key=True)
  name = Column('name', String(50), unique=True)
  year = Column('year', String(4))
  awards = Column('awards', Integer)
  nominations = Column('nominations', Integer)
  # image = relationship('MoviePoster', back_populates="movie")

class MoviePoster(Base):
  __tablename__ = 'movie_poster'

  id = Column(Integer, primary_key=True)
  # movie_id = Column(Integer, ForeignKey('movie.id'))
  src = Column('src', Text)
  alt_text = Column('alt_text', String(50))
  # movie = relationship("Movie", back_populates="movie_poster")