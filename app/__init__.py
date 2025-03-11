from flask import Flask
from flask_restful import Api

from app.routes.favorites_routes import (
    AdminFavoriteMoviesResource,
    FavoriteMoviesResource,
)
from app.routes.movies_routes import MoviesResource


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(MoviesResource, "/movies/popular")
    api.add_resource(FavoriteMoviesResource, "/movies/favorites", endpoint="favorites")
    api.add_resource(FavoriteMoviesResource, "/movies/favorites/<int:movie_id>")
    api.add_resource(
        AdminFavoriteMoviesResource, "/admin/users/<int:user_id>/favorites"
    )

    return app
