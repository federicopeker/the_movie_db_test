from flask import jsonify, make_response, request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from app.models.movie import Movie
from app.services.favorite_service import FavoriteService
from app.utils.auth import token_required
from app.utils.cache import Cache


class FavoriteMoviesResource(Resource):
    @token_required("USER")
    def post(self, current_user):
        """Add a movie to favorites"""
        try:
            data = request.get_json()
            if not data:
                raise BadRequest("Request body is missing")

            id = data.get("id")
            title = data.get("title")
            release_date = data.get("release_date")

            if not id or not title or not release_date:
                raise BadRequest(
                    "Missing required fields: 'id', 'title' and 'release_date'"
                )

            movie = Movie(id, title, release_date, 0)
            FavoriteService.add_favorite(current_user["id"], movie)

            response = {
                "success": True,
                "message": "Movie added to favorites",
                "data": movie.to_dict(),
            }
            return make_response(jsonify(response), 201)

        except BadRequest as e:
            return make_response(jsonify({"success": False, "error": str(e)}), 400)
        except Exception:
            return make_response(
                jsonify({"success": False, "error": "Internal Server Error"}), 500
            )

    @token_required("USER")
    def delete(self, current_user, movie_id):
        """Remove a movie from favorites"""
        try:
            FavoriteService.remove_favorite(current_user["id"], movie_id)

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "message": f"Movie {movie_id} removed from favorites",
                    }
                ),
                200,
            )

        except Exception:
            return make_response(
                jsonify({"success": False, "error": "Internal Server Error"}), 500
            )

    @token_required("USER")
    def get(self, current_user):
        """Get the user's favorite movies"""
        try:
            cache = Cache()
            cache_key = f"favorites_{current_user['id']}"
            cached_response = cache.get_cached_response(cache_key)

            if cached_response:
                return make_response(
                    jsonify({"success": True, "data": cached_response}), 200
                )

            sort_by = request.args.get("sort_by", "release_date,rating").split(",")
            sorted_favorites = FavoriteService.get_favorites_sorted(
                current_user["id"], sort_by
            )

            if sorted_favorites:
                cache.cache_response(cache_key, sorted_favorites)

            return make_response(
                jsonify({"success": True, "data": sorted_favorites}), 200
            )

        except Exception:
            return make_response(
                jsonify({"success": False, "error": "Internal Server Error"}), 500
            )

    @token_required("USER")
    def patch(self, current_user, movie_id):
        """Update the rating of a favorite movie"""
        try:
            data = request.get_json()
            if not data or "rating" not in data:
                raise BadRequest("Missing required field: 'rating'")

            new_rating = data["rating"]
            if not isinstance(new_rating, int) or not (0 <= new_rating <= 5):
                raise BadRequest("Rating must be an integer between 0 and 5")

            FavoriteService.update_rating(current_user["id"], movie_id, new_rating)

            return make_response(
                jsonify(
                    {
                        "success": True,
                        "message": f"Rating for movie {movie_id} updated to {new_rating}",
                    }
                ),
                200,
            )

        except BadRequest as e:
            return make_response(jsonify({"success": False, "error": str(e)}), 400)
        except Exception:
            return make_response(
                jsonify({"success": False, "error": "Internal Server Error"}), 500
            )


class AdminFavoriteMoviesResource(Resource):
    @token_required("ADMIN")
    def delete(self, current_user, user_id):
        """Remove all favorites for a user (Admin only)"""
        try:
            FavoriteService.remove_all_favorites(user_id)
            return make_response(
                jsonify(
                    {
                        "success": True,
                        "message": f"All favorites for user {user_id} removed",
                    }
                ),
                200,
            )
        except Exception:
            return make_response(
                jsonify({"success": False, "error": "Internal Server Error"}), 500
            )
