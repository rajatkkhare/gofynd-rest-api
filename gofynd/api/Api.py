from flask import request
from flask_restful import Api as _Api


class Api(_Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def error_router(self, original_handler, e):
        """ Override original error_router to only handle HTTPExceptions. """
        if request.path.startswith('/api'):
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler
        return original_handler(e)
