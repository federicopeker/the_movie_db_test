from flask import jsonify, make_response
from flask_restful import Resource

from app.adapters.movie_service import MovieService
from app.utils.cache import Cache


class MoviesResource(Resource):
    def get(self):
        """Get popular movies from TheMovieDB"""
        try:
            cache = Cache()
            cache_key = "movies_popular"
            cached_response = cache.get_cached_response(cache_key)

            if cached_response:
                return make_response(
                    jsonify({"success": True, "data": cached_response}), 200
                )

            movies = MovieService.get_popular_movies()

            if movies:
                cache.cache_response(cache_key, movies)

            return make_response(jsonify({"success": True, "data": movies}), 200)
        except Exception:
            return make_response(
                jsonify({"success": False, "error": "Internal Server Error"}), 500
            )
