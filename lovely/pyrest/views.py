from pyramid.httpexceptions import (HTTPMethodNotAllowed,
                                    HTTPError,
                                    HTTPUnsupportedMediaType,
                                    HTTPNotAcceptable)
from pyramid.response import Response
from pyramid.exceptions import PredicateMismatch
from errors import Errors
from lovely.pyrest.validation import validate_schema
from lovely.pyrest.settings import (
    DEFAULT_VIEW_SETTINGS,
    DEFAULT_HELP_MESSAGE,
    JSONP_SETTINGS,
    get_jsonp_param_name
)
import json
import functools


def decorate_view(view, args):
    """ Adds a decorator to a `pyramid` view.
    The decorator validates the `schema` and executes the additional
    `validators`.

    :param view: the view to decorate
    :param args: the args to use for the decoration
    """
    def get_help_message(request):
        """ Checks if 'help' is set as query parameter in a request.
        If so, the schema will be displayed as a documentation
        to show which query parameters can (or must) be present in a reqeust.

        If and API endpoint does not accept any query parameters
        (i.e. schema is empty) an appropriate message will be returned.
        """
        schema = args.get('schema')
        response = None
        if 'help' in request.GET:
            if schema:
                response = schema
            else:
                response = DEFAULT_HELP_MESSAGE
        return response

    def wrapper(request):
        help = args.get('help', DEFAULT_VIEW_SETTINGS.get('help'))
        if help:
            response = get_help_message(request)
            # do not validate anything else. show the help imediately.
            if response is not None:
                return response

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
            if is_jsonp_request(request):
                # if JSONP is requested return a HTTP 200 OK and create an
                # error message. Pyramid wraps the message with given
                # JSONP function name.
                response = create_json_errors(request.errors)
                response['http_status'] = request.errors.status
                return response
            else:
                return JSONError(request.errors, request.errors.status)
        response = _view(request)
        return response

    functools.wraps(wrapper)
    return wrapper

def is_jsonp_request(request):
    return get_jsonp_param_name() in request.GET


def create_json_errors(errors):
    errors = {
        'status': 'error',
        'errors': errors
    }
    return errors


class JSONError(HTTPError):

    def __init__(self, errors, status=400):
        body = create_json_errors(errors)
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
