# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from database.models import Movie, MoviePoster, db_connect, create_table

class WikipediaScraperPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        movie = Movie()
        # movie_poster = MoviePoster(movie=movie)

        movie.name = item['name']
        movie.year = item['year']
        movie.awards = item['awards']
        movie.nominations = item['nominations']

        # movie_poster.src = item['image']['src']
        # movie_poster.alt_text = item['image']['alt_text']
        # movie.image = movie_poster

        try:
            session.add(movie)
            # session.add(movie_poster)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
