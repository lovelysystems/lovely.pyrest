
DEFAULT_VIEW_SETTINGS = {
    'renderer': 'jsonp',    # default views' renderer
    'help': True            # enable 'help' by default
}


# Default message if a request with query parameter `help` is processed
# and the request does not have defined a schema.
DEFAULT_HELP_MESSAGE = {'help': 'This API endpoint does not accept any '
                                + 'specific query parameters'}

# ---------------------
#   JSONP_SETTINGS
# ---------------------

"""
We do add a JSONP renderer at startup
(lovely.pyrest.__init__.add_custom_config()). The renderer requires a
parameter name. If this parameter is given in a request as query parameter the
JSONP renderer will be triggered.

Since we cannot retrieve the specified parameter name by default when we need
it (e.g. in lovely.pyrest.views.py) we need to store the parameter name
(set_jsonp_param_name() and get_jsonp_param_name()).
"""

# Default query parameter name for a JSONP request.
DEFAULT_JSONP_PARAM_NAME = 'callback'

JSONP_SETTINGS = {
    # 'param_name' can be specified in the '.ini' file with following
    # identifier.
    'param_name_ini': 'lovely.pyrest.jsonp.param_name',

    # Override this to set a custom query parameter name using the '.ini' file.
    # Use 'set_jsonp_param_name(...)' to override the value.
    'param_name': DEFAULT_JSONP_PARAM_NAME
}


def set_jsonp_param_name(settings):
    """
    Set the specified JSONP query parameter name.
    The 'param_name' is being set to 'param_name_ini' if given;
    DEFAULT_JSONP_PARAM_NAME otherwise.

    Call the function once at startup time (e.g. lovely.pyrest.__init__).
    @settings
        pyramid config settings.
    """
    JSONP_SETTINGS['param_name'] = settings.get(
        JSONP_SETTINGS['param_name_ini'],
        DEFAULT_JSONP_PARAM_NAME
    )


def get_jsonp_param_name():
    """
    Return the specified JSONP query parameter name.
    If the parameter is set in the '.ini' file, the custom parameter is
    used; otherwise the default parameter is used.
    """
    return JSONP_SETTINGS['param_name']
