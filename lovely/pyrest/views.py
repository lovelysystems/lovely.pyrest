# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH
from pyramid.httpexceptions import (HTTPMethodNotAllowed,
                                    HTTPError,
                                    HTTPUnsupportedMediaType,
                                    HTTPNotAcceptable)
from pyramid.response import Response
from pyramid.exceptions import PredicateMismatch
from errors import Errors
from lovely.pyrest.validation import validate_schema
import json
import functools


def decorate_view(view, args):
    """ Adds a decorator to a `pyramid` view.
    The decorator validates the `schema` and executes the additional
    `validators`.

    :param view: the view to decorate
    :param args: the args to use for the decoration
    """

    def wrapper(request):
        _view = view
        validators = args.get('validators', ())
        schema = args.get('schema')
        # check schema
        if schema:
            validate_schema(request, schema)
        # execute validators
        for validator in validators:
            validator(request)
        # the validators or validate_schema() adds errors to the request if
        # validaton fails.
        # check if there are errors and return an ErrorResponse if so
        if len(request.errors) > 0:
            return JSONError(request.errors, request.errors.status)
        response = _view(request)
        return response
    functools.wraps(wrapper)
    return wrapper



class JSONError(HTTPError):

    def __init__(self, errors, status=400):
        body = {'status': 'error', 'errors': errors}
        # HTTPError is derived from Response
        super(Response, self).__init__(json.dumps(body))
        self.status = status
        self.content_type = 'application/json'


def get_fallback_view(service):
    """ The fallback_view doesn't have any predicates, except the service route.
        If there is no other view in the `service` which matches the requests
        predicates, pyramid will use this fallback view because it will
        always match the predicates of the request.
        Instead of raising the PredicateMismatch error which would cause a 404
        response, the view checks the `content_type` and `access_header`
        predicate. So it's possible to return a correct error instead of 404.
    """

    # the fallback view returns a correct error at predicate
    # mismatch
    def _fallback(request):
        if request.method not in service.methods:
            errors = Errors()
            errors.add(
                'method',
                'The method %s is not allowed for this resource' % request.method
            )
            return JSONError(errors, HTTPMethodNotAllowed.code)
        # Check other predicates like content type
        for method, _, args in service.definitions:
            if method != request.method:
                continue
            # Check Accept header
            if 'accept' in args:
                supported = service.acceptables(request.method)
                if not request.accept.best_match(supported):
                    request.errors.status = HTTPNotAcceptable.code
                    request.errors.add(
                        'header',
                        'Accept header should be one of %s' % supported
                    )
                    return JSONError(request.errors, request.errors.status)
            # Check Content-Type header
            if 'content_type' in args:
                supported = service.content_types(request.method)
                if request.content_type not in supported:
                    request.errors.status = HTTPUnsupportedMediaType.code
                    request.errors.add(
                        'header',
                        'Content-Type header should be one of %s' % supported)
                    return JSONError(request.errors, request.errors.status)
        raise PredicateMismatch(service.name)

    return _fallback
