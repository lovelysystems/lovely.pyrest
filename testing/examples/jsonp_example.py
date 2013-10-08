from lovely.pyrest.service import Service

svc = Service(name='svc', path='/svc')


@svc.get(renderer='json')
def get(request):
    return {'title': 'Hello World!'}
