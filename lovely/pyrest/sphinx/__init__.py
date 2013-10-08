from lovely.pyrest.sphinx.schema import SchemaDirective
from lovely.pyrest.sphinx.validators import ValidatorsDirective
from lovely.pyrest.sphinx.service import ServiceDirective


def setup(sphinx):
    sphinx.add_directive('service', ServiceDirective)
    sphinx.add_directive('schema', SchemaDirective)
    sphinx.add_directive('validators', ValidatorsDirective)
