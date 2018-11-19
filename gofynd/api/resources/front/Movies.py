from flask_restful import Resource, reqparse
from gofynd.api.common import jwt_required, api_resp
from gofynd.models.Director import Director
from gofynd.models.Genre import Genre
from gofynd.models.GenreMovie import GenreMovie
from gofynd.models.Movie import Movie


class Movies(Resource):
    @jwt_required
    def get(self):
        args = reqparse.RequestParser().add_argument('page').add_argument('director') \
            .add_argument('genre').add_argument('name').add_argument('imdb_score').parse_args()
        page = int(args['page']) if args['page'] else None
        movies = Movie.query
        if args['name']:
            movies = movies.filter(Movie.name.like("%"+args['name'].strip()+"%"))
        if args['imdb_score']:
            movies = movies.filter(Movie.imdb_score >= args['imdb_score']).order_by(Movie.imdb_score.desc())
        if args['director']:
            movies = movies.join(Director).filter(Director.name.like("%"+args['director'].strip()+"%"))
        if args['genre']:
            movies = movies.join(GenreMovie).join(Genre).filter(Genre.name.like("%"+args['genre'].strip()+"%"))
        movies = movies.paginate(per_page=33, page=page, error_out=False)
        serialize_movies = [movie.serialize for movie in movies.items]
        return api_resp(200, 'success', {'movies': serialize_movies, 'total': movies.total, 'pages': movies.pages, 'current_page': movies.page, 'has_prev': movies.has_prev, 'has_next': movies.has_next})
