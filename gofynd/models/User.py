from gofynd.app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_super = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, _email=None, _password=None, _first_name='', _last_name=''):
        self.email = _email if _email else None
        if _password:
            self.password = _password
            self.set_password()
        self.first_name = _first_name.strip()
        self.last_name = _last_name.strip()

    def __str__(self):
        return '{0} {1}: {2}'.format(self.first_name, self.last_name, self.email)

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.first_name, self.last_name, self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_user(cls, _email=None, _id=None):
        if _email:
            return cls.query.filter_by(email=_email).first()
        if _id:
            return cls.query.filter_by(id=_id).first()

    def set_password(self):
        self.password = generate_password_hash(self.password)
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)
