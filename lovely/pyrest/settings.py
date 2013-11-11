
DEFAULT_VIEW_SETTINGS = {
    'renderer': 'jsonp',    # default views' renderer
    'help': True            # enable 'help' by default
}


# Default message if a request with query parameter `help` is processed
# and the request does not have defined a schema.
DEFAULT_HELP_MESSAGE = {'help': 'This API endpoint does not accept any '
                                + 'specific query parameters'}


JSONP_SETTINGS = {
    # 'param_name' can be specified in the '.ini' file with following
    # identifier.
    'param_name_ini': 'lovely.pyrest.jsonp.param_name',

    # Default query parameter name. Will be overriden if 'param_name_ini' is
    # set.
    'param_name': 'callback',
}
