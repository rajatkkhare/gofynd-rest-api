from gofynd.app import db


class GenreMovie(db.Model):
    __tablename__ = 'genre_movies'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
