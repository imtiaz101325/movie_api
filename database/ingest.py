import datetime
import logging
import requests
import pandas as pd
from io import StringIO
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Movie, MovieGenre, MovieRating, db_connect, create_table

def ingest_data():
    movie_request = requests.get('https://school.cefalolab.com/assignment/python/movies.csv', verify=False)
    movie_raw_data = StringIO(movie_request.text)
    movies = pd.read_csv(movie_raw_data)

    rating_request = requests.get('https://school.cefalolab.com/assignment/python/ratings.csv', verify=False)
    rating_raw_data = StringIO(rating_request.text)
    ratings = pd.read_csv(rating_raw_data)

    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    for _, row in movies.iterrows():
        title = row['title'][:-7]
        year = row['title'][-7:].replace(' (', '').replace(')', '')

        movie = session.query(Movie).filter_by(
            name = title, year = year
        ).first()

        if movie is not None:
            genres = row['genres'].split('|')

            for genre in genres:
                movie.genre.append(MovieGenre(genre = genre))
            filtered_ratings = ratings[ratings['movieId'] == row['movieId']]
            for _, rating_row in filtered_ratings.iterrows():
                movie.rating.append(MovieRating(user_id = rating_row['userId'], rating = rating_row['rating'], timestamp = datetime.datetime.fromtimestamp(rating_row['timestamp'])))


            try:
                session.add(movie)
                session.commit()

            except:
                session.rollback()
                raise
        else:
            logging.info(f'{title} ({year}) did not match any movies in the database')
    
    session.close()
