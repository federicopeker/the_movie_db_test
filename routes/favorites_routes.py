from flask import jsonify
from flask_restful import Resource

from app.models.favorite import FavoriteMoviesDB
from app.utils.auth import token_required


class FavoriteMoviesResource(Resource):
    @token_required("USER")
    def post(self, current_user, movie_id):
        FavoriteMoviesDB.add_favorite(current_user["id"], movie_id)
        return jsonify({"message": f"Movie {movie_id} added to favorites"})

    @token_required("USER")
    def delete(self, current_user, movie_id):
        FavoriteMoviesDB.remove_favorite(current_user["id"], movie_id)
        return jsonify({"message": f"Movie {movie_id} removed from favorites"})

    @token_required("USER")
    def get(self, current_user):
        favorite_movies = FavoriteMoviesDB.get_favorites(current_user["id"])
        return jsonify({"result": favorite_movies})
