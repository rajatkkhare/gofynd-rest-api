from flask_restful import Resource, abort
from gofynd.api.RequestParser import RequestParser
from gofynd.api.common import api_resp
from gofynd.models.User import User
from datetime import datetime, timedelta
from instance.settings import SECRET_KEY
import jwt, re


class Auth(Resource):
    def post(self, action):
        if action == 'login':
            return self.login()
        if action == 'signup':
            return self.signup()
        return abort(404)

    def login(self):
        parser = RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('email', required=True, help='The email field is required.')
        parser.add_argument('password', required=True, help='The password field is required.')
        args = parser.parse_args()
        user = User.find_user(_email=args.email)
        if user:
            if user.check_password(args.password) and user.is_active:
                token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow()+timedelta(days=30),
                                    'iat': datetime.utcnow()}, SECRET_KEY)
                return api_resp(200, 'success', {'access_token': token.decode('UTF-8')})
        return api_resp(400, 'error', {'email': 'Incorrect email address and / or password.'})

    def signup(self):
        parser = RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('email', required=True, help='The email field is required.')
        parser.add_argument('first_name', required=True, help='The first name field is required.')
        parser.add_argument('last_name', required=True, help='The last name field is required.')
        parser.add_argument('password', required=True, help='The password field is required.')
        args = parser.parse_args()
        if not re.match(r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$", args.email):
            return api_resp(400, 'error', {'email': 'Please enter a valid email address.'})
        if User.query.filter_by(email=args.email).first():
            return api_resp(400, 'error', {'email': 'Email has already been taken.'})
        if len(args.password) < 5:
            return api_resp(400, 'error', {'password': 'Password must be at least 5 characters.'})
        user = User(args.email, args.password, args.first_name, args.last_name)
        user.is_active = True
        if user.save():
            return api_resp(200, 'success', {'detail': 'Account created successfully.'})
        return api_resp(409, 'error', {'detail': 'There has been some error.'})
