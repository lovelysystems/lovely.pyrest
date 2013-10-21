from docutils import nodes
from docutils.parsers.rst import Directive
from lovely.pyrest.service import get_services
from importlib import import_module
from lovely.pyrest.sphinx.helpers import create_node, trim
from lovely.pyrest.sphinx.schema import SchemaDirective
from lovely.pyrest.sphinx.validators import ValidatorsDirective


class ServiceDirective(Directive):
    """ The Service directive renders all services defined in a module """

    has_content = True
    required_arguments = 1

    def run(self):
        module = self.arguments[0]
        import_module(module)
        rendered = []
        settings = self.state.document.settings
        services = get_services()
        for service in services:
            service_id = "service_%d" % settings.env.new_serialno('service')
            rendered.append(ServiceDirective.render(service, service_id))
        return rendered

    @staticmethod
    def render(service, service_id):
        service_node = nodes.section(ids=[service_id])
        title = "%s service - %s" % (service.name, service.path)
        service_node += nodes.title(text=title)

        if service.description is not None:
            service_node += create_node(trim(service.description))

        for method, view, args in service.definitions:
            method_id = "%s_%s" % (service_id, method)
            method_node = nodes.section(ids=[method_id])
            method_node += nodes.title(text=method)

            # Render Accept Header documentation
            acceptables = service.acceptables(method)
            if len(acceptables) > 0:
                accept = 'Accept: ' + ', '.join(acceptables)
                method_node += create_node(accept)

            # Render Content-Type Header documentation
            content_types = service.content_types(method)
            if len(content_types) > 0:
                ct = 'Content-Types: ' + ', '.join(content_types)
                method_node += create_node(ct)

            if 'schema' in args:
                method_node += SchemaDirective.render_schema(service,
                                                             method,
                                                             service_id)

            if 'validators' in args:
                method_node += ValidatorsDirective.render(service,
                                                          method,
                                                          service_id)
            service_node += method_node
        return service_node
