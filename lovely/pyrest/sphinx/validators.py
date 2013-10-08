from docutils.parsers.rst import Directive
from importlib import import_module
from lovely.pyrest.service import get_service
from lovely.pyrest.sphinx.helpers import create_node, trim, empty_node
from docutils import nodes


class ValidatorsDirective(Directive):
    """ The Validators directive renders the validators docstrings """

    has_content = True
    required_arguments = 3

    def run(self):
        module, svc, method = self.arguments
        import_module(module)
        service = get_service(svc)
        service_id = "service_%d" % self.state.document.settings.env.new_serialno('service')
        return [ValidatorsDirective.render(service,
                                           method,
                                           service_id)]

    @staticmethod
    def render(service, method, service_id):
        """ Renders the validators list of the service """
        if not service:
            return empty_node()
        validators = service.get_argument('validators', method)
        if not validators:
            return empty_node()

        rendered_nodes = []
        # render every validator and add it to the `rendered_nodes`
        # the result of rendering is not none
        for validator in validators:
            node = ValidatorsDirective.render_validator(validator)
            if node is not None:
                rendered_nodes.append(node)

        if len(rendered_nodes) > 0:
            validators_id = "service_%s_%s_%s" % (service_id,
                                                  method,
                                                  'validators')
            validator_section = nodes.section(ids=[validators_id])
            validator_title = nodes.title(text='Validation:')
            # add the rendered_nodes to the validator_title
            for node in rendered_nodes:
                validator_title += node
            validator_section += validator_title
            return validator_section
        # Return an empty node if none of the validators has a docstring
        return empty_node()

    @staticmethod
    def render_validator(validator):
        doc = validator.__doc__
        if doc is not None:
            doc = trim(doc)
            return create_node(doc)
        return None
