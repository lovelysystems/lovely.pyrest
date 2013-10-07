from lovely.pyrest.service import Service

article = Service(name='article', path='/article')

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
        "properties": {
            "id": {
                "type": "string"
            },
            "categories": {
                "type": "array",
                "required": False,
                "items": {
                    "enum": ["news", "sports", "politics"]
                }
            }
        }
    }
}


@article.post(schema=schema)
def post(request):
    """ Save an article """
    return {'stored': 'ok'}


@article.get(schema=schema)
def get(request):
    """ Save an article """
    return {'stored': 'ok'}
