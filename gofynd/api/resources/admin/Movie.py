from flask_restful import Resource, reqparse
from gofynd.api.common import jwt_required, api_resp, is_admin
from gofynd.app import db
from gofynd.models.Director import Director
from gofynd.models.Genre import Genre
from gofynd.models.GenreMovie import GenreMovie
from gofynd.models.Movie import Movie as MovieModel


class Movie(Resource):
    @jwt_required
    @is_admin
    def get(self, movie_id):
        movie = MovieModel.query.filter_by(id=movie_id).first()
        if movie:
            return api_resp(200, 'success', {'movie': movie.serialize})
        return api_resp(404, 'error', {'detail': 'No record found.'})

    @jwt_required
    @is_admin
    def put(self, movie_id):
        args = reqparse.RequestParser()\
            .add_argument('name').add_argument('imdb_score')\
            .add_argument('popularity').add_argument('director')\
            .add_argument('genres', action='append').parse_args()
        movie = MovieModel.query.filter_by(id=movie_id).first()
        if movie:
            director = Director.query.filter_by(name=args['director']).first()
            if not director:
                director = Director()
                director.name = args['director']
                director.save()
            genres = []
            if args.get('genres'):
                for genre_name in args.get('genres'):
                    if genre_name.strip():
                        genre = Genre.query.filter_by(name=genre_name.strip()).first()
                        if not genre:
                            genre = Genre()
                            genre.name = genre_name.strip()
                            genre.save()
                            genres.append(genre)
                        else:
                            genres.append(genre)
                GenreMovie.query.filter_by(movie_id=movie_id).delete()
            movie.name = args.get('name').strip()
            movie.imdb_score = args.get('imdb_score')
            movie.popularity = args.get('popularity')
            movie.director = director
            if len(genres):
                movie.genres.extend(genres)
            if movie.save():
                return api_resp(200, 'success', {'movie': movie.serialize})
        return api_resp(404, 'error', {'detail': 'No record found.'})

    @jwt_required
    @is_admin
    def delete(self, movie_id):
        movie = MovieModel.query.filter_by(id=movie_id).first()
        if movie:
            GenreMovie.query.filter_by(movie_id=movie_id).delete()
            MovieModel.query.filter_by(id=movie_id).delete()
            db.session.commit()
            return api_resp(200, 'success', {'detail': 'Movie deleted successfully.'})
        return api_resp(404, 'error', {'detail': 'No record found.'})
