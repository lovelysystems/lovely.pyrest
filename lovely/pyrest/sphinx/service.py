from docutils import nodes
from docutils.parsers.rst import Directive
from lovely.pyrest.rest import get_services
from importlib import import_module
from lovely.pyrest.sphinx.helpers import create_node, trim
from pyramid import paster
from pyramid.config import Configurator
import json
import venusian


def convert_to_list(value):
    if value is None:
        return []
    return [v.strip() for v in value.split(',')]


class ServiceDirective(Directive):
    """ The Service directive renders all services defined in a module """

    has_content = True
    required_arguments = 0
    optional_arguments = 1

    option_spec = {'services': convert_to_list}

    def run(self):
        # Check if the pyramid config file is set, if souse paster to manage
        # imports
        conf_file = self.pyramid_conf()
        if conf_file:
            paster.get_app(conf_file)
        else:
            # instantiate a pyramid configurator
            config = Configurator()
            module_str = self.arguments[0]
            # import the module
            module = import_module(module_str)
            # check if the module has an `includeme` method and call it
            # because the base route must be added
            if hasattr(module, 'includeme'):
                module.includeme(config)
            config.commit()
            # scan the module for services
            scanner = venusian.Scanner(config=config)
            scanner.scan(module)
        rendered = []
        # fetch all services
        services = get_services()
        # if the services option is set render only the named services
        names = self.options.get('services')
        if names:
            services = [s for s in services if s.baseRouteName in names]
        for service in services:
            service_id = "service_%d" % self.serialno('service')
            rendered.append(ServiceDirective.render(service, service_id))
        return rendered

    def serialno(self, ident):
        """ Renders a serialno for a given term
            Should be overwritten in tests
        """
        settings = self.state.document.settings
        return settings.env.new_serialno(ident)

    def pyramid_conf(self):
        conf = self.state.document.settings.env.config
        return conf['pyramid_conf']

    @staticmethod
    def render(service, service_id):
        service_node = nodes.section(ids=[service_id])
        title = "%s service" % service.baseRouteName
        service_node += nodes.title(text=title)

        if service.description is not None:
            service_node += create_node(trim(service.description))

        for pattern, route_kw, view_kw, func, schema in service.methods:
            method = route_kw.get('request_method', 'GET')
            method_id = "%s_%s" % (service_id, method)
            method_node = nodes.section(ids=[method_id])
            method_title = "%s - %s" % (method, pattern)
            method_node += nodes.title(text=method_title)
            # render description from docstring
            desc = func.__doc__
            if desc:
                method_node += create_node(trim(desc))

            accept = route_kw.get('accept')
            content_type = route_kw.get('content_type')

            # Render Accept Header documentation
            if accept:
                accept_desc = 'Accept: %s' % accept
                method_node += create_node(accept_desc)
            # Render Content-Type Header documentation
            if content_type:
                content_desc = 'Content-Type: %s' % content_type
                method_node += create_node(content_desc)

            # Render Validator
            if schema:
                schema_id = "%s_%s_%s" % (service_id,
                                          method,
                                          'validator')
                node = nodes.section(ids=[schema_id])
                title = nodes.title(text='Data Schema:')
                text = json.dumps(schema, indent=4)
                # prefix every line with a pipe, so the rst conversation returns a
                # line_block where the spaces are preserved
                text = '\n'.join(['| ' + l for l in text.splitlines()])
                node += title
                node += create_node(trim(text))

                method_node += node
            service_node += method_node
        return service_node
