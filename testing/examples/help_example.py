from lovely.pyrest.service import Service

svc = Service(name='svc', path='/svc')

schema = {
    "query": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "required": False
            }
        }
    }
}

@svc.get(schema=schema)
def get(request):
    return {'title': 'Hello World!'}
