from flask import jsonify, request
from flask_restful import Resource

from app.models.movie import Movie
from app.services.favorite_service import FavoriteService
from app.utils.auth import token_required
from app.utils.cache import Cache


class FavoriteMoviesResource(Resource):
    @token_required("USER")
    def post(self, current_user):
        data = request.get_json()
        release_date = data.get("release_date")
        movie_id = data.get("movie_id")
        title = data.get("title")
        movie = Movie(movie_id, title, release_date, 0)

        FavoriteService.add_favorite(current_user["id"], movie)
        return jsonify({"message": f"Movie {movie_id} added to favorites"})

    @token_required("USER")
    def delete(self, current_user, movie_id):
        FavoriteService.remove_favorite(current_user["id"], movie_id)
        return jsonify({"message": f"Movie {movie_id} removed from favorites"})

    @token_required("USER")
    def get(self, current_user):
        cache = Cache()
        cache_key = f"favorites_{current_user['id']}"
        cached_response = cache.get_cached_response(cache_key)
        if cached_response:
            return jsonify({"result": cached_response})

        sorted_favorites = FavoriteService.get_favorites(current_user["id"])
        if sorted_favorites:
            cache.cache_response(cache_key, sorted_favorites)
        return jsonify({"result": sorted_favorites})

    @token_required("USER")
    def patch(self, current_user, movie_id):
        data = request.get_json()
        new_rating = data.get("rating")
        if new_rating is not None:
            FavoriteService.update_rating(current_user["id"], movie_id, new_rating)
            return jsonify(
                {"message": f"Rating for movie {movie_id} updated to {new_rating}"}
            )
        return {"error": "Rating not provided"}, 400


class AdminFavoriteMoviesResource(Resource):
    @token_required("ADMIN")
    def delete(self, current_user, user_id):
        FavoriteService.remove_all_favorites(user_id)
        return jsonify({"message": f"All favorites for user {user_id} removed"})
