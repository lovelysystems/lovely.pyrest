from lovely.pyrest.sphinx.service import ServiceDirective


def setup(sphinx):
    sphinx.add_directive('service', ServiceDirective)
    sphinx.add_config_value('pyramid_conf', None, 'env')
