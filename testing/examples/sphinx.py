from lovely.pyrest.rest import RestService, rpcmethod_route
from lovely.pyrest.validation import validate

# Create a schema to validate the body
schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        }
    }
}


@RestService('article')
class ArticleService(object):
    """ Create and read articles """

    @rpcmethod_route(request_method='POST',
                     content_type='application/json')
    def create(self, data):
        """ Update article """
        return {'created': '123'}

    @rpcmethod_route(request_method='GET',
                     accept='application/json')
    @validate(schema)
    def get(self, id):
        """ Returns the article """
        return {'title': 'the title'}


def includeme(config):
    config.add_route('article', '/article', static=True)
