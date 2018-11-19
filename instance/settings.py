import os

DEBUG = os.environ.get('DEBUG_STATUS', True)
SECRET_KEY = 'KdP0g7HY5IsERsAKPGOhwW08sumvdixU4oRAGWTn8zE'  # os.urandom(24)
URL_BASE = os.environ.get('BASE_URL', 'http://localhost:5000')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "mysql://root:root@localhost/gofynd")
SQLALCHEMY_TRACK_MODIFICATIONS = False
