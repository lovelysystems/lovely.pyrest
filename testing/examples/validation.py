from lovely.pyrest.service import Service

article = Service(name='article', path='/article')


def validate_query(request):
    """ Check if the id field is set """
    if not 'id' in request.GET:
        request.errors.add('query',
                           'Parameter `id` is missing')
        request.errors.status = 400


@article.get(validators=[validate_query])
def get(request):
    return {'status': 'success'}
