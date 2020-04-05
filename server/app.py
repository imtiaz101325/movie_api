from flask import Flask
from flask_restful import Api, Resource
from sqlalchemy.orm import scoped_session, sessionmaker
from database.models import Movie, db_connect, create_table
from marshmallow import Schema, fields

engine = db_connect()
create_table(engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

app = Flask(__name__)
api = Api(app)

class MoviePosterSchema(Schema):
    class Meta:
        fields = ('src', 'alt_text', 'movie')
        exclude = ('movie',)

class MovieSchema(Schema):
    class Meta:
        fields = ('name', 'year', 'awards', 'nominations', 'image', 'directors', 'producers', 'stars')
        exclude = ('image', 'directors', 'producers', 'stars')

    image = fields.Nested(MoviePosterSchema)

class Movies(Resource):
    def get(self):
        movies_schema = MovieSchema(many=True)
        return movies_schema.dump(db_session().query(Movie).all())

api.add_resource(Movies, '/')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)