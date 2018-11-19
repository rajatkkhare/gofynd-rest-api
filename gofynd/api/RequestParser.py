from flask import request
from flask_restful import abort
from flask_restful.reqparse import RequestParser as _RequestParser
from werkzeug import exceptions


class RequestParser(_RequestParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_args(self, req=None, strict=False):
        """Parse all arguments from the provided request and return the results
        as a Namespace

        :param req:
        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        """
        if req is None:
            req = request

        namespace = self.namespace_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            abort(400, errors=errors, status=400, message='error')

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest('Unknown arguments: %s'
                                        % ', '.join(req.unparsed_arguments.keys()))

        return namespace
