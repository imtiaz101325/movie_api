from flask import Flask, render_template
from flask_restful import Api, Resource, abort, request

from marshmallow import Schema, fields

from sqlalchemy.sql import func
from sqlalchemy.orm import scoped_session, sessionmaker
from database.models import Movie, MovieRating, db_connect, create_table

engine = db_connect()
create_table(engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

app = Flask(__name__)
api = Api(app)

class MoviePosterSchema(Schema):
    class Meta:
        fields = ('src', 'alt_text', 'movie')
        exclude = ('movie',)

class MovieResultSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'year', 'awards', 'nominations', 'image', 'directors', 'producers', 'stars')
        exclude = ('directors', 'producers', 'stars')

    image = fields.Nested(MoviePosterSchema)

class MoviePaginatedSchema(Schema):
    class Meta:
        fields = ('start', 'limit', 'total', 'previous', 'next', 'results')

    results = fields.Nested(MovieResultSchema, many=True)

def get_paginated_list(start, limit):
    count = db_session().query(Movie).count()
    if (count < start):
        abort(404, message=f'Not enough movies to start at {start}')

    res = {}
    res['start'] = start
    res['limit'] = limit
    res['total'] = count
    res['results'] = db_session().query(Movie).limit(limit).offset(start).all()

    return res

class MovieList(Resource):
    def get(self):
        args = request.args
        start = int(args.get('start', default=1))
        limit = int(args.get('limit', default=10))
        movies_schema = MoviePaginatedSchema()
        return movies_schema.dump(get_paginated_list(start, limit))

class SingleMovie(Resource):
    def get(self, movie_id):
        movies_schema = MovieResultSchema()
        movie = db_session().query(Movie).filter_by(id = movie_id).first()
        if movie is None:
            abort(404, message='Movie dose not exist')
        return movies_schema.dump(movie)

class Rating(Resource):
    def get(self, movie_id):
        movie = db_session().query(Movie).filter_by(id = movie_id).first()
        if movie is None:
            abort(404, message='Movie dose not exist')
        
        ratings = db_session().query(
            func.avg(MovieRating.rating).label('avg_rating'),
            func.count(MovieRating.user_id).label('user_count')
        ).filter_by(movie_id = movie.id).first()

        return {
            'avg_rating': ratings[0] and round(ratings[0], 2),
            'users': ratings[1],
            'name': movie.name
        }

class Search(Resource):
    def get(self):
        args = request.args
        name = args.get('name', default='')

        movies_schema = MovieResultSchema(many=True)
        return movies_schema.dump(
            db_session().query(Movie).filter(
                Movie.name.contains(name)
            ).all()
        )

@app.route('/')
def index():
    return render_template('base.html', title='Home')

api.add_resource(MovieList, '/api/movies')
api.add_resource(SingleMovie, '/api/movies/<movie_id>')
api.add_resource(Rating, '/api/movies/<movie_id>/rating')
api.add_resource(Search, '/api/search')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)