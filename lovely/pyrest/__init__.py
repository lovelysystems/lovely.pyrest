# Shared Source Software
# Copyright (c) 2013 Lovely Systems GmbH

from lovely.pyrest.predicates import ContentTypePredicate
from lovely.pyrest.views import get_fallback_view, decorate_view
from pyramid.events import NewRequest
from errors import Errors
import copy

__version__ = "0.0.4"


def add_service(config, service):
    """ Registers a service at config """
    services = config.registry.setdefault('services', {})
    services[service.path] = service
    # keep track of the registered routes
    registered_routes = []
    for method, view, args in service.definitions:
        args = copy.deepcopy(args)  # make a copy of the dict to not modify it
        args['request_method'] = method
        decorated_view = decorate_view(view, dict(args))
        # remove args which are unknown by pyramid
        for item in ('validators', 'schema'):
            if item in args:
                del args[item]

        # if the route is new, add the route and add the
        # `fallback_view` for this route
        if service.path not in registered_routes:
            config.add_route(service.name, service.path)
            config.add_view(view=get_fallback_view(service),
                            route_name=service.name)
            registered_routes.append(service.path)
            config.commit()
        config.add_view(view=decorated_view, route_name=service.name, **args)


def wrap_request(event):
    """ Creates an empty errors list and adds it to the request """
    request = event.request
    if not hasattr(request, 'errors'):
        request.errors = Errors()


# The includeme function will be called after including
# this module:
# config.include('lovely.pyrest')
def includeme(config):
    config.add_directive('add_service', add_service)
    config.add_subscriber(wrap_request, NewRequest)
    config.add_view_predicate('content_type', ContentTypePredicate)
