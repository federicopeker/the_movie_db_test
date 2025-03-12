from flask_restful import Resource

from app.adapters.movie_service import MovieService


class MoviesResource(Resource):
    def get(self):
        return MovieService.get_popular_movies()
