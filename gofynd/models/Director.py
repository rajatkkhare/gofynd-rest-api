from gofynd.app import db
from sqlalchemy.orm import backref


class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    movies = db.relationship('Movie', backref=backref('director', lazy='joined'), lazy='dynamic')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
