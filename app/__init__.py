from flask import Flask
from flask_restful import Api

from app.movies_routes import MoviesResource


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(MoviesResource, "/movies/popular")

    return app
