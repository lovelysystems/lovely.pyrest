=========================
Tests for rest decorators
=========================

RestService
===========

The RestService is a decorator to decorate a class as a rest service. In
detail it attaches a callback to venusian. Whenever venusian runs a scanner
the previously attached callback gets executed.

Let's say we like to decorate the class called `Service`::

    >>> class Service(object):
    ...     pass

Before we are able to decorate the class successfully some testing setup has
to be done. venusian requires a proper module to attach the callback for. So
we need to create a stubmodule and add our service to that module::

    >>> class stubmodule:
    ...     __name__ = "stubmodule"
    ...     __path__ = "stubmodule"
    ...     Service = Service

    >>> import sys
    >>> sys.modules['stubmodule'] = stubmodule

The current execution frame has to run within this module as well::

    >>> frame = sys._getframe(0)
    >>> frame.f_globals['__name__'] = 'stubmodule'
    >>> frame.f_locals['__module__'] = 'stubmodule'

Finally we can decorate the class `Service` with RestService::

    >>> from lovely.pyrest.rest import RestService
    >>> _ = RestService('base')(Service)

Now run the venusian scan to get our decorator executed. The decorator requires
the pyramid config which has to be passed to the venusian scanner::

    >>> from pyramid.urldispatch import Route
    >>> class RouteMapper():
    ...     route = Route('base', '/base')
    ...     def get_route(self, name):
    ...         return self.route

    >>> class Config():
    ...    routes_mapper = RouteMapper()
    ...    def with_package(self, module):
    ...        return self
    ...    def get_routes_mapper(self):
    ...        return self.routes_mapper
    ...    def add_route(self, *args, **kwargs):
    ...        factory = kwargs.get('factory')
    ...        self.routes_mapper.route = Route(*args, factory=factory)
    ...        print 'add_route', args, kwargs
    ...    def add_view(self, *args, **kwargs):
    ...        print 'add_view', args, kwargs

    >>> import venusian
    >>> config = Config()
    >>> scanner = venusian.Scanner(config=config)
    >>> scanner.scan(stubmodule)

Since our decorated service does not provide any method the decorator does not
do anything. However, one requirement of the decorator is the existence of the
base route. An exception will be raised if the route was not found.  Possible
reasons for this exception can be either the route has not been defined or the
config has not been commited before calling config.scan()::

    >>> config.routes_mapper.route = None
    >>> scanner.scan(stubmodule)
    Traceback (most recent call last):
    BaseRouteNotFoundException

Now let's provide the service with a decorated method called `foo` and an
undecorated method called `bar`. Note: A route with a proper pattern is
required::

    >>> config.routes_mapper.route = Route('base', 'pattern')

    >>> from lovely.pyrest.rest import rpcmethod_route
    >>> class Service(object):
    ...     @rpcmethod_route()
    ...     def foo(self):
    ...         return "foo"
    ...     def bar(self):
    ...         return "bar"
    >>> stubmodule.Service = Service

    >>> _ = RestService('base')(Service)

    >>> scanner.scan(stubmodule)
    add_route ('base.foo@pattern', 'pattern') {'request_method': 'GET'}
    add_view () {'mapper': <class 'lovely.pyrest.rest.ViewMapper'>, 'attr': 'foo', 'renderer': 'json', 'route_name': 'base.foo@pattern', 'view': <class 'stubmodule.Service'>}

Sometimes it is required to pass arguments to the view. For this case use the
decorator `rpcmethod_view`. Same as `rpcmethod_route` this decorator will mark
a method as a rpc method::

    >>> from lovely.pyrest.rest import rpcmethod_view
    >>> class Service(object):
    ...     @rpcmethod_view(permission="Sample")
    ...     def foo(self):
    ...         return "foo"
    ...     def bar(self):
    ...         return "bar"
    >>> stubmodule.Service = Service

    >>> _ = RestService('base')(Service)

    >>> scanner.scan(stubmodule)
    add_route ('base.foo@pattern', 'pattern') {'request_method': 'GET'}
    add_view () {'mapper': <class 'lovely.pyrest.rest.ViewMapper'>, 'attr': 'foo', 'permission': 'Sample', 'route_name': 'base.foo@pattern', 'renderer': 'json', 'view': <class 'stubmodule.Service'>}

It's also possible to combine them::

    >>> class Service(object):
    ...     @rpcmethod_route(request_method='POST')
    ...     @rpcmethod_view(permission="Sample")
    ...     def foo(self):
    ...         return "foo"
    ...     def bar(self):
    ...         return "bar"
    >>> stubmodule.Service = Service

    >>> _ = RestService('base')(Service)

    >>> scanner.scan(stubmodule)
    add_route ('base.foo@pattern', 'pattern') {'request_method': 'POST'}
    add_view () {'mapper': <class 'lovely.pyrest.rest.ViewMapper'>, 'attr': 'foo', 'permission': 'Sample', 'route_name': 'base.foo@pattern', 'renderer': 'json', 'view': <class 'stubmodule.Service'>}


Service wide configuration
--------------------------

Configurations on the base route will get applied to each internally created
route. Any keyword argument passed to the RestService decorator will get applied to
the view::

    >>> class Service(object):
    ...     @rpcmethod_route()
    ...     def foo(self):
    ...         return "foo"

    >>> stubmodule.Service = Service

    >>> class StubFactory():
    ...     pass

    >>> config.add_route('base', '/base', factory=StubFactory)
    add_route ('base', '/base') {'factory': <class stubmodule.StubFactory at 0x...>}

    >>> _ = RestService('base', permission='admin')(Service)

    >>> scanner.scan(stubmodule)
    add_route ('base.foo@/base', '/base') {'request_method': 'GET', 'factory': <class stubmodule.StubFactory at 0x...>}
    add_view () {'mapper': <class 'lovely.pyrest.rest.ViewMapper'>, 'attr': 'foo', 'permission': 'admin', 'route_name': 'base.foo@/base', 'renderer': 'json', 'view': <class 'stubmodule.Service'>}


rpcmethod_route
===============

This is a decorator to mark methods of a class as rpc methods. In detail this
decorator puts given kwargs to the decorated method onto the variable
`__rpc_method_route__`. All given keywords will get passed to the
config.add_route call::

    >>> def func():
    ...     return "a"

    >>> _ = rpcmethod_route(foo="bar")(func)
    >>> func.__rpc_method_route__
    {'foo': 'bar'}


rpcmethod_view
==============

This is a decorator to mark methods of a class as rpc methods. In detail this
decorator puts given kwargs to the decorated method onto the variable
`__rpc_method_view__`. All given keywords will get passed to the
config.add_view call::

    >>> def func():
    ...     return "a"

    >>> _ = rpcmethod_view(foo="bar")(func)
    >>> func.__rpc_method_view__
    {'foo': 'bar'}


ViewMapper
==========

The ViewMapper is responsible to pass request specific data into the handler of
the request as arguments. The passed keywords get built from the
request.matchdict (data is provided by the url palceholder), the request.params
and the request.json_body::

    >>> class Request():
    ...     matchdict = {}
    ...     params = {}
    ...     json_body = {}

    >>> from lovely.pyrest.rest import ViewMapper
    >>> mapper = ViewMapper(attr="method")

If none of the previously mentioned attributes contains any keyword arguments
the signature of the invoked method does not have to contain any parameter::

    >>> class View():
    ...     def __init__(self, request):
    ...         pass
    ...     def method(self):
    ...         print 'called'

    >>> mapper(View)(None, Request())
    called

If the request provides some of the mentioned keywords the signature of the
method must match::

    >>> class View():
    ...     def __init__(self, request):
    ...         pass
    ...     def method(self, **kwargs):
    ...         print kwargs

    >>> Request.matchdict['matchdict'] = "1"
    >>> Request.params['params'] = "2"
    >>> Request.json_body['json_body'] = {"data": 123}

    >>> mapper(View)(None, Request())
    {'params': '2', 'json_body': {'data': 123}, 'matchdict': '1'}
