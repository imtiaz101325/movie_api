from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text
)

Base = declarative_base()

def db_connect():
    return create_engine('sqlite:///database/movies.db')

def create_table(engine):
    Base.metadata.create_all(engine)

movie_director_accociation_table = Table('movie_director_association', Base.metadata,
  Column('movie_id', Integer, ForeignKey('movies.id')),
  Column('director_id', Integer, ForeignKey('directors.id'))
)

movie_producer_accociation_table = Table('movie_producer_association', Base.metadata,
  Column('movie_id', Integer, ForeignKey('movies.id')),
  Column('producer_id', Integer, ForeignKey('producers.id'))
)

movie_star_accociation_table = Table('movie_star_association', Base.metadata,
  Column('movie_id', Integer, ForeignKey('movies.id')),
  Column('star_id', Integer, ForeignKey('stars.id'))
)

class Movie(Base):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  name = Column('name', String(100))
  year = Column('year', String(4))
  awards = Column('awards', String(10))
  nominations = Column('nominations', String(10))
  image = relationship('MoviePoster', uselist=False, back_populates='movie')
  genre = relationship('MovieGenre', back_populates='movie')
  rating = relationship('MovieRating', back_populates='movie')
  directors = relationship(
    'Director',
    secondary=movie_director_accociation_table,
    back_populates='movies'
  )
  producers = relationship(
    'Producer',
    secondary=movie_producer_accociation_table,
    back_populates='movies'
  )
  stars = relationship(
    'Star',
    secondary=movie_star_accociation_table,
    back_populates='movies'
  )

class MovieGenre(Base):
  __tablename__ = 'genres'

  id = Column(Integer, primary_key=True)
  movie_id = Column(Integer, ForeignKey('movies.id'))
  genre = Column('genre', String(10))
  movie = relationship('Movie', back_populates='genre')

class MovieRating(Base):
  __tablename__ = 'ratings'

  id = Column(Integer, primary_key=True)
  movie_id = Column(Integer, ForeignKey('movies.id'))
  user_id = Column('user_id', Integer)
  rating = Column('rating', Float)
  timestamp = Column('timestamp', DateTime)
  movie = relationship('Movie', back_populates='rating')

class MoviePoster(Base):
  __tablename__ = 'movie_posters'

  id = Column(Integer, primary_key=True)
  movie_id = Column(Integer, ForeignKey('movies.id'))
  src = Column('src', Text)
  alt_text = Column('alt_text', Text)
  movie = relationship("Movie", back_populates='image')

class Person(object):
  id = Column(Integer, primary_key=True)
  name = Column('name', Text, unique=True)

class Director(Person, Base):
  __tablename__ = 'directors'

  movies = relationship(
    'Movie',
    secondary=movie_director_accociation_table,
    back_populates='directors'
  )

class Producer(Person, Base):
  __tablename__ = 'producers'

  movies = relationship(
    'Movie',
    secondary=movie_producer_accociation_table,
    back_populates='producers'
  )

class Star(Person, Base):
  __tablename__ = 'stars'

  movies = relationship(
    'Movie',
    secondary=movie_star_accociation_table,
    back_populates='stars'
  )