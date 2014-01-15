from pyramid.response import Response
from pyramid.exceptions import NotFound
from lovely.pyrest.validation import ValidationException


class PageNotFound(NotFound):
    """ Extended NotFound class"""


def bad_request(exc, request):
    request.response.status = 400
    return {
            'status': "ERROR",
            'reason': exc.message
            }


def forbidden(request):
    request.response.status = 403
    return {
            'status': "ERROR"
            }


def notfound(request):
    request.response.status = 404
    return {
            'status': "ERROR"
            }


def internal_server_error(exc, request):
    request.response.status = 500
    return {
            'status': "ERROR",
            'reason': exc.message
            }


def pagenotfound(request):
    return Response("This site doesn't exist", status="404 Not Found")


def includeme(config):
    config.add_view(pagenotfound, context=PageNotFound)
    config.add_view(bad_request, renderer='json',
                    context=ValidationException)
    config.add_view(forbidden, renderer='json',
                    context='pyramid.exceptions.Forbidden')
    config.add_view(notfound, renderer='json',
                    context='pyramid.exceptions.NotFound')
    config.add_view(internal_server_error, renderer='json',
                    context=Exception)
