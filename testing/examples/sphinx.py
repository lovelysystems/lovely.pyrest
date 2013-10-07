from lovely.pyrest.service import Service

articles = Service(name='article', path='/article/{id}')


def article_exists(request):
    """ Validates that the article exists """
    pass


@articles.get(validators=[article_exists], accept='application/json')
def get(request):
    """ Returns an article """
    return {'title': 'the title'}


# Create a schema to validate the body
schema = {
    "body": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            }
        }
    },
    "query": {
        "type": "object",
        "properites": {
            "id": {
                "type": "string"
            }
        }
    }
}


@articles.post(schema=schema, content_type='application/json')
def post(request):
    """ Save an article """
    return {'created': '123'}
