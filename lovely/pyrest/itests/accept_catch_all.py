from lovely.pyrest.service import Service

"""
This module contains a service definitions and a couple of views to explain
the 'accept_catch_all' view annotation parameter.
"""

service1 = Service('myService1', '/service/1')

@service1.get()
def svc1_get(request):
    return {'test': 'succeeded'}


service2 = Service('myService2', '/service/2')

@service2.get(accept_catch_all=False)
def svc2_get(request):
    return {'test': 'succeeded'}
