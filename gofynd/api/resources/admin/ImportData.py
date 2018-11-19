from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from gofynd.api.common import jwt_required, api_resp, is_admin
from gofynd.models.Director import Director
from gofynd.models.Genre import Genre
from gofynd.models.Movie import Movie
from gofynd.utils import random_generator
import os, json


class ImportData(Resource):
    @jwt_required
    @is_admin
    def post(self):
        data_file = request.files.get('import_data')
        if data_file:
            filename = secure_filename(data_file.filename)
            filename = random_generator(40) + '.' + filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join('./storage', filename)
            data_file.save(file_path)
            data = open(file_path, 'r')
            data = json.load(data)
            for row in data:
                director_name = row.get('director').strip()
                director_exist = Director.query.filter_by(name=director_name).first()
                if not director_exist:
                    director = Director()
                    director.name = director_name
                    director.save()
                for genre_name in row.get('genre'):
                    genre_exist = Genre.query.filter_by(name=genre_name.strip()).first()
                    if not genre_exist:
                        genre = Genre()
                        genre.name = genre_name.strip()
                        genre.save()
            for row in data:
                movie = Movie()
                movie.name = row.get('name').strip()
                movie.imdb_score = row.get('imdb_score')
                movie.popularity = row.get('99popularity')
                director = Director.query.filter_by(name=row.get('director').strip()).first()
                movie.director = director
                genres = [genre.strip() for genre in row.get('genre')]
                if len(genres):
                    genres = Genre.query.filter(Genre.name.in_(genres))
                    movie.genres.extend(genres)
                movie.save()
            if os.path.isfile(file_path):
                os.remove(file_path)
            return api_resp(200, 'success', {'detail': 'Data imported successfully.'})
        return api_resp(409, 'error', {'detail': 'No file found.'})
