from gofynd.app import db
from sqlalchemy.orm import backref
from .GenreMovie import GenreMovie


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    movies = db.relationship('Movie', secondary='genre_movies',
                             backref=backref('genres', lazy='joined'), lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
