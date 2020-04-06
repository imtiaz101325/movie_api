# -*- coding: utf-8 -*-
from pathlib import Path
import logging
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from database.models import Movie, MoviePoster, Director, Producer, Star, db_connect, create_table

class WikipediaScraperPipeline(object):
    def __init__(self):
        logging.info('Remove existing database.')
        path = Path('./database/movies.db')
        if path.exists():
            path.unlink()

        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        movie = Movie()
        movie_poster = MoviePoster(movie=movie)

        movie.name = item['name']
        movie.year = item['year']
        movie.awards = item['awards']
        movie.nominations = item['nominations']

        movie_poster.src = item['image']['src']
        movie_poster.alt_text = item['image']['alt_text']
        movie.image = movie_poster

        persons = [{
            'item_key': 'directed_by',
            'model': Director,
            'movie_key': 'directors'
        },{
            'item_key': 'produced_by',
            'model': Producer,
            'movie_key': 'producers'
        },{
            'item_key': 'starring',
            'model': Star,
            'movie_key': 'stars'
        }]

        for person_data in persons:
            for person in item[person_data['item_key']]:
                person_exists = session.query(person_data['model']).filter_by(name = person).first()
                if person_exists is not None:
                    getattr(movie, person_data['movie_key']).append(person_exists)
                else:
                    getattr(movie, person_data['movie_key']).append(person_data['model'](name= person))

        try:
            session.add(movie)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
