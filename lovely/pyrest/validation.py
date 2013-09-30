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


def validate_schema(request, schema):
    # validate schema
    query_schema = schema.get("query")
    if query_schema is not None:
        try:
            # convert GET parameters to a dictionary which can be validated
            params = {k: request.GET[k] for k in request.GET}
            validictory.validate(params, query_schema,
                                 format_validators=FORMAT_VALIDATORS)
        except ValueError, error:
            request.errors.add('query',
                               error.message)
