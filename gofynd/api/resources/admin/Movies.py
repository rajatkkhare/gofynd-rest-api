from flask_restful import Resource, reqparse
from gofynd.api.common import jwt_required, api_resp, is_admin
from gofynd.models.Director import Director
from gofynd.models.Genre import Genre
from gofynd.models.Movie import Movie


class Movies(Resource):
    @jwt_required
    @is_admin
    def get(self):
        args = reqparse.RequestParser().add_argument('page').parse_args()
        page = int(args['page']) if args['page'] else None
        movies = Movie.query.paginate(per_page=3, page=page, error_out=False)
        serialize_movies = [movie.serialize for movie in movies.items]
        return api_resp(200, 'success', {'movies': serialize_movies, 'total': movies.total, 'pages': movies.pages, 'current_page': movies.page, 'has_prev': movies.has_prev, 'has_next': movies.has_next})

    @jwt_required
    @is_admin
    def post(self):
        args = reqparse.RequestParser()\
            .add_argument('name').add_argument('imdb_score')\
            .add_argument('popularity').add_argument('director')\
            .add_argument('genres', action='append').parse_args()
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
        movie = Movie()
        movie.name = args.get('name').strip()
        movie.imdb_score = args.get('imdb_score')
        movie.popularity = args.get('popularity')
        movie.director = director
        if len(genres):
            movie.genres.extend(genres)
        if movie.save():
            return api_resp(200, 'success', {'movie': movie.serialize})
        return api_resp(409, 'error', {'detail': 'There has been some error.'})
