from lovely.pyrest.sphinx.service import ServiceDirective


def setup(sphinx):
    sphinx.add_directive('service', ServiceDirective)
