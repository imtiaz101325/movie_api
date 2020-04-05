from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)



if __name__ == '__main__':
    app.run(debug=True)