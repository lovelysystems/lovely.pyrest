from lovely.pyrest.predicates import ContentTypePredicate
from lovely.pyrest.views import get_fallback_view, decorate_view
from lovely.pyrest.settings import (
    JSONP_SETTINGS,
    set_jsonp_param_name,
    get_jsonp_param_name
)
from pyramid.events import NewRequest
from errors import Errors
from pyramid.renderers import JSONP
import copy

__version__ = "0.1.3"


def add_service(config, service):
    """ registers the views for a service """
    # register the route
    config.add_route(service.name, service.path)
    # create the fallback view
    config.add_view(view=get_fallback_view(service),
                    route_name=service.name)
    for method, view, args in service.definitions:
        args = copy.deepcopy(args)  # make a copy of the dict to not modify it
        args['request_method'] = method
        decorated_view = decorate_view(view, dict(args))
        # remove args which are unknown by pyramid
        for item in ('validators', 'schema', 'jsonp', 'help'):
            if item in args:
                del args[item]
        config.add_view(view=decorated_view, route_name=service.name, **args)
    config.commit()


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
    add_custom_config(config)


def add_custom_config(config):
    """ Custom configuration parameters in your .ini file
    will be handled here.
    """
    settings = config.get_settings()

    # Add JSONP support
    # If param_name is set as qeury parameter in a request it will trigger
    # the JSONP transformation.
    # 'callback' will be set as default if `param_name` is not specified in
    # the '.ini' file.
    set_jsonp_param_name(settings)
    config.add_renderer('jsonp', JSONP(param_name=get_jsonp_param_name()))
