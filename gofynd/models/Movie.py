from gofynd.app import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    imdb_score = db.Column(db.Float)
    popularity = db.Column(db.Float)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name, 'imdb_score': self.imdb_score, '99popularity': self.popularity, 'director': self.director.name, 'genres': [genre.name for genre in self.genres]}
