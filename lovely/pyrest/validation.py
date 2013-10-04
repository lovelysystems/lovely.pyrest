# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH

from rfc3987 import get_compiled_pattern
from validictory import ValidationError
import validictory

URL = get_compiled_pattern('^%(URI)s$')


def validate_format_url(validator, fieldname, value, format_option):
    if URL.match(value) is None:
        raise ValidationError("Value '%s' of field '%s' is not an url" % (value, fieldname))


FORMAT_VALIDATORS = {
    "url": validate_format_url
}
FORMAT_VALIDATORS.update(validictory.validator.DEFAULT_FORMAT_VALIDATORS)


def validate_schema(request, schema):
    # validate schema
    query_schema = schema.get("query")
    if query_schema is not None:
        try:
            # convert GET parameters to a dictionary which can be validated
            params = {k: request.GET[k] for k in request.GET}
            for prop, o in query_schema.get('properties').iteritems():
                # if schema type is array, split the parameter string by comma
                # and replace the original string value with the generated
                # array for the validation
                if o.get('type') == 'array':
                    v = params.get(prop)
                    if v is not None:
                        params[prop] = v.split(",")
            # for convenience remember the params_dict on the request
            request.params_dict = params
            validictory.validate(params, query_schema,
                                 format_validators=FORMAT_VALIDATORS)
        except ValueError, error:
            request.errors.add('query',
                               error.message)
    body_schema = schema.get("body")
    if body_schema is not None:
        try:
            json_body = request.json_body
            validictory.validate(json_body, body_schema,
                                 format_validators=FORMAT_VALIDATORS)
        except ValueError, error:
            request.errors.add('body',
                               error.message)
