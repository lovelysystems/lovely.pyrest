import inspect
import logging
import venusian
from pyramid.config import predicates

log = logging.getLogger(__name__)

SERVICES = {}


def get_services():
    return list(SERVICES.values())


class ViewMapper(object):
    """ Mapper to pass request specific data to view method
    """

    ROOT_ARRAY_KW_NAME = "items"

    def __init__(self, **kw):
        self.attr = kw.get('attr')

    def __call__(self, view):
        def wrapper(context, request):
            def json_body(request):
                """ Failsave function to access request.json_body
                """
                try:
                    body = request.json_body
                    if isinstance(body, list):
                        return {self.ROOT_ARRAY_KW_NAME: body}
                    return body
                except:
                    return {}

            def mapply(func, request):
                """ This function passes request.matchdict, request.params and
                request.json_body as kwargs to the given function
                """
                kw = {}
                # add kwargs from matchdict
                kw.update(request.matchdict)

                # add kwargs from request params
                kw.update(dict(list(request.params.items())))

                # add kwargs from request body
                kw.update(json_body(request))

                return func(**kw)

            inst = view(request)
            meth = getattr(inst, self.attr)
            return mapply(meth, request)
        return wrapper


class BaseRouteNotFoundException(Exception):
    """ A exception to indicate that the required base route was not found

    Possible reasons for this exception:
        - the route has not been defined
        - the config has not been commited before calling config.scan()
    """


class RestService(object):
    """ Decorator for REST API classes

    @RestService('users')
    class UserService(object):

        def __init__(self, request):
            self.request = request

        @rpcmethod(route_suffix='/{id}', request_method='PUT')
        def edit(self, id, data):
            # code goes here

    def includeme(config):
        config.add_route('users', '/users', static=True)
    """

    venusian = venusian

    def reverse_engineer_route(self, route):
        kw = {}
        if route.factory:
            kw['factory'] = route.factory
        if route.pregenerator:
            kw['pregenerator'] = route.pregenerator

        def xhr(p):
            kw['xhr'] = p.val

        def path_info(p):
            kw['path_info'] = p.val.pattern

        def request_param(p):
            kw['request_param'] = p.val[0]

        def header(p):
            kw['header'] = p.text().split(" ", 1)[-1]

        def accept(p):
            kw['accept'] = p.val

        def custom_predicates(p):
            if not 'custom_predicates' in kw:
                kw['custom_predicates'] = []
            kw['custom_predicates'].append(p.func)

        def request_method(p):
            kw['request_method'] = p.val[0]
        predicate_map = {predicates.XHRPredicate: xhr,
                         predicates.PathInfoPredicate: path_info,
                         predicates.RequestParamPredicate: request_param,
                         predicates.HeaderPredicate: header,
                         predicates.AcceptPredicate: accept,
                         predicates.CustomPredicate: custom_predicates,
                         predicates.RequestMethodPredicate: request_method,
                        }
        for p in route.predicates:
            predicate_map[p.__class__](p)
        return kw

    def __init__(self, baseRouteName, **view_kwargs):
        self.baseRouteName = baseRouteName
        self.serviceName = None
        self.view_kwargs = view_kwargs
        # All methods of the services get registered here for sphinx autodoc
        self.methods = []

    def __call__(self, wrapped):
        def callback(context, name, service):
            config = context.config.with_package(info.module)
            # load the base route to get it's resolved pattern
            mapper = config.get_routes_mapper()
            baseRoute = mapper.get_route(self.baseRouteName)
            if baseRoute is None:
                raise BaseRouteNotFoundException
            # get default route arguments
            route_defaults = self.reverse_engineer_route(baseRoute)

            # get all rpcmethod decorated members
            def isRESTMethod(obj):
                return (inspect.ismethod(obj)
                        and (hasattr(obj, '__rpc_method_route__') or
                             hasattr(obj, '__rpc_method_view__'))
                    )
            methods = inspect.getmembers(service, isRESTMethod)
            # register the service
            self.serviceName = '@'.join((self.baseRouteName, baseRoute.path))
            SERVICES[self.serviceName] = self
            self.description = service.__doc__
            # if the module is used multiple times for documentation generation
            # the service get registered a few times so reset methods here.
            self.methods = []
            # loop through all decorated methods and add a route and a view
            # for it
            for (methodName, method) in methods:
                route_kw = {}
                route_kw.update(route_defaults)
                if hasattr(method, '__rpc_method_route__'):
                    route_kw.update(method.__rpc_method_route__)
                # allow http method GET by default
                if 'request_method' not in route_kw:
                    route_kw['request_method'] = 'GET'
                view_kw = {}
                view_kw.update(self.view_kwargs)
                if hasattr(method, '__rpc_method_view__'):
                    view_kw.update(method.__rpc_method_view__)
                route_name = ('.'.join((self.baseRouteName, methodName))
                              + '@'
                              + baseRoute.path
                             )
                pattern = baseRoute.pattern + route_kw.pop('route_suffix', '')
                # Register method
                validator = None
                if method.__func__.__name__ == 'validation_wrapper':
                    # index 2 of func_closure is the schema param of the
                    # validate method in the tuple, not accessible via keyword
                    validator = method.__func__.__closure__[2].cell_contents
                self.methods.append(
                            (pattern, route_kw, view_kw, method, validator))
                config.add_route(route_name, pattern, **route_kw)
                config.add_view(view=service,
                                route_name=route_name,
                                attr=methodName,
                                mapper=ViewMapper,
                                renderer='json',
                                **view_kw)
                log.debug('Adding REST method %s %s (%s)',
                          route_kw['request_method'], pattern, route_name)

        info = self.venusian.attach(wrapped, callback, category='restservice',
                                    depth=1)
        return wrapped


def rpcmethod_route(context_factory=None, **kwargs):
    """ Decorator to mark methods of classes decorated with `RestService`
    as member of the REST Service
    """

    def wrapper(f):
        f.context_factory = context_factory
        f.__rpc_method_route__ = kwargs
        return f
    return wrapper


def rpcmethod_view(context_factory=None, **kwargs):
    """ Decorator to mark methods of classes decorated with `RestService`
    as member of the REST Service
    """

    def wrapper(f):
        f.context_factory = context_factory
        f.__rpc_method_view__ = kwargs
        return f
    return wrapper
