from docutils.parsers.rst import Directive
from docutils import nodes
from importlib import import_module
from lovely.pyrest.service import get_service
from lovely.pyrest.sphinx.helpers import create_node, trim, empty_node
import json


class SchemaDirective(Directive):
    """ The Schema directive renders the information about GET-Parameter and
        JSON-Body of a specific service. """

    has_content = True
    required_arguments = 3

    def run(self):
        module, svc, method = self.arguments
        import_module(module)
        service = get_service(svc)
        env = self.state.document.settings.env
        service_id = "service_%d" % env.new_serialno('service')
        return [SchemaDirective.render_schema(service,
                                              method,
                                              service_id)]

    @staticmethod
    def render_schema(service, method, service_id):
        """ Renders schema information of a service """
        # check if service is not null
        if not service:
            return empty_node()
        schema = service.get_argument('schema', method)
        # check that the schema exists
        if not schema:
            return empty_node()
        schema_id = "%s_%s_%s" % (service_id,
                                  method,
                                  'schema')
        node = nodes.section(ids=[schema_id])
        # if the schema contains a `query` schema render GET-Parameters
        # documentation:
        # <name>: <required>, <type>, <description>, <other arguments>
        if 'query' in schema and 'properties' in schema['query']:
            title = nodes.title(text='GET-Parameters:')
            node +=title
            properties = schema['query']['properties']
            for param, spec in properties.iteritems():
                prop_node = nodes.list_item()
                desc = "%s: " % param
                extras = []
                # Check if required is true
                # and add (required | optional)
                if spec.get('required', True):
                    extras.append('required')
                else:
                    extras.append('optional')
                # Check if the type is set and add it as second
                # parameter
                if 'type' in spec:
                    extras.append('' + spec['type'])
                # Check if the description is set and add it as
                # third parameter
                if 'description' in spec:
                    extras.append('' + spec['description'])

                # add the other fields
                for k, v in spec.iteritems():
                    if k in ['type', 'description', 'required']:
                        continue
                    extras.append(' %s: %s' % (k, v))
                desc += ', '.join(extras)
                prop_node += nodes.inline(text=desc)

                node += prop_node
        # if the schema has a `body` schema convert it to string and
        # insert it into the documentation
        if 'body' in schema:
            body_schema = schema['body']
            title = nodes.title(text='JSON Body:')
            text = json.dumps(body_schema, indent=4)
            # prefix every line with a pipe, so the rst conversation returns a
            # line_block where the spaces are preserved
            text = '\n'.join(['| ' + l for l in text.splitlines()])
            node += title
            node += create_node(trim(text))
        return node
