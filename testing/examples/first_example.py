from lovely.pyrest.rest import RestService, rpcmethod_route
from lovely.pyrest.validation import validate, ValidationException


ARTICLES = {}


# Create a schema to validate the body
schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "content": {
            "type": "string",
            "required": False
        },
    }
}


@RestService('article')
class ArticlesService(object):
    """ Create and read articles """

    def __init__(self, request):
        self.request = request

    @rpcmethod_route(request_method='POST')
    @validate(schema)
    def post(self, data):
        id = len(ARTICLES)
        ARTICLES[id] = data
        return {'stored': id}

    @rpcmethod_route(route_suffix='/{id}')
    def get(self, id):
        return ARTICLES.get(id)


def bad_request(exc, request):
    request.response.status = 400
    return {
            'status': "ERROR",
            'reason': exc.message
            }


def includeme(config):
    config.add_route('article', '/article', static=True)
    config.add_view(bad_request, renderer='json',
                    context=ValidationException)
