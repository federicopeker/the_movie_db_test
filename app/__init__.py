from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from app.routes.favorites_routes import (
    AdminFavoriteMoviesResource,
    FavoriteMoviesResource,
)
from app.routes.movies_routes import MoviesResource


def create_app():
    app = Flask(__name__, static_folder="../static")
    api = Api(app)

    api.add_resource(MoviesResource, "/movies")
    api.add_resource(FavoriteMoviesResource, "/favorites", endpoint="favorites")
    api.add_resource(FavoriteMoviesResource, "/favorites/<int:movie_id>")
    api.add_resource(
        AdminFavoriteMoviesResource, "/admin/users/<int:user_id>/favorites"
    )
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/openapi.yaml"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Favorite Movies API"}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
