from lovely.pyrest.service import Service

articles = Service(name='article', path='/article/{id}')

ARTICLES = {}


def article_exists(request):
    """ A Validator the verify that the article exists """
    _id = request.matchdict['id']
    if _id not in ARTICLES:
        desc = "Article with id %s does not exist" % _id
        request.errors.add('uri', desc)  # Add an error if validation fails
        request.errors.status = 404  # Set the error status code


@articles.get(validators=[article_exists])
def get(request):
    """ Returns an article """
    return ARTICLES.get(request.matchdict['id'])


# Create a schema to validate the body
schema = {
    "body": {
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
}


@articles.post(schema=schema)
def post(request):
    """ Save an article """
    _id = request.matchdict['id']
    return {'stored': _id}
