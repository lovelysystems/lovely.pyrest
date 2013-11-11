
DEFAULT_VIEW_SETTINGS = {
    'renderer': 'jsonp',    # default views' renderer
    'help': True            # enable 'help' by default
}


JSONP_SETTINGS = {
    # 'param_name' can be specified in the '.ini' file with following
    # identifier.
    'param_name_ini': 'lovely.pyrest.jsonp.param_name',

    # Default query parameter name. Will be overriden if 'param_name_ini' is
    # set.
    'param_name': 'callback',
}
