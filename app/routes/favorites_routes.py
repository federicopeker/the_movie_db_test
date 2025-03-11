from flask import jsonify, request
from flask_restful import Resource

from app.models.favorite import FavoriteMoviesDB
from app.utils.auth import token_required


class FavoriteMoviesResource(Resource):
    @token_required("USER")
    def post(self, current_user, movie_id):
        data = request.get_json()
        release_date = data.get("release_date")
        rating = data.get("rating", 0)
        FavoriteMoviesDB.add_favorite(
            current_user["id"], movie_id, release_date, rating
        )
        return jsonify({"message": f"Movie {movie_id} added to favorites"})

    @token_required("USER")
    def delete(self, current_user, movie_id):
        FavoriteMoviesDB.remove_favorite(current_user["id"], movie_id)
        return jsonify({"message": f"Movie {movie_id} removed from favorites"})

    @token_required("USER")
    def get(self, current_user):
        sorted_favorites = FavoriteMoviesDB.get_favorites(current_user["id"])
        return jsonify({"result": sorted_favorites})

    @token_required("USER")
    def patch(self, current_user, movie_id):
        data = request.get_json()
        new_rating = data.get("rating")
        if new_rating is not None:
            FavoriteMoviesDB.update_rating(current_user["id"], movie_id, new_rating)
            return jsonify(
                {"message": f"Rating for movie {movie_id} updated to {new_rating}"}
            )
        return {"error": "Rating not provided"}, 400
