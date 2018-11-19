from werkzeug.local import LocalProxy
from flask import _request_ctx_stack


def api_resp(status: int, message: str, data: dict='', headers: dict='') -> object:
    if status == 200:
        return {'status': status, 'message': message, 'data': data}, status, headers
    return {'status': status, 'message': message, 'errors': data}, status, headers


def api_failure_resp(status: int, message: str, errors: dict='') -> object:
    return {'status': status, 'message': message, 'errors': errors}


def api_errors():
    return {
        'MethodNotAllowed':
            api_failure_resp(405, 'error', {'detail': 'The method is not allowed for the requested URL.'}),
        'NotFound':
            api_failure_resp(404, 'error', {'detail': 'The requested URL was not found on the server.'})
    }


current_user = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'cur_user', None))


def jwt_required(func):
    from flask import request
    from functools import wraps
    import jwt
    from gofynd.models.User import User
    from instance.settings import SECRET_KEY

    @wraps(func)
    def decorator(*args, **kwargs):
        auth_header_value = request.headers.get('Authorization', None)
        if not auth_header_value:
            return api_resp(401, 'error', {'detail': 'Request does not contain an access token.'})
        parts = auth_header_value.split()
        if parts[0].lower() != 'JWT'.lower():
            return api_resp(401, 'error', {'detail': 'Unsupported authorization type.'})
        elif len(parts) == 1:
            return api_resp(401, 'error', {'detail': 'Token missing.'})
        elif len(parts) > 2:
            return api_resp(401, 'error', {'detail': 'Token must not contain spaces.'})
        try:
            data = jwt.decode(parts[1], SECRET_KEY, verify=False)
        except jwt.InvalidTokenError:
            return api_resp(401, 'error', {'detail': 'Invalid token.'})
        else:
            _request_ctx_stack.top.cur_user = cur_user = User.query.filter_by(
                id=data['user_id']).filter_by(is_active=True).first()
            if not cur_user:
                return api_resp(401, 'error', {'detail': 'User does not exist.'})
            return func(*args, **kwargs)
    return decorator


def is_admin(func):
    from functools import wraps

    @wraps(func)
    def decorator(*args, **kwargs):
        if not current_user.is_admin:
            return api_resp(403, 'error', {'detail': 'You don\'t have permission to access.'})
        return func(*args, **kwargs)
    return decorator
