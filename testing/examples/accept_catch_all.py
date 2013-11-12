from lovely.pyrest.service import Service

svc = Service(name='svc', path='/svc')


@svc.get(accept="text/plain", accept_catch_all=False)
def get(request):
    return "'title': 'Hello World!'"

@svc.get(accept='application/json')
def get_json(request):
    return {'title': 'Hello World!'}
