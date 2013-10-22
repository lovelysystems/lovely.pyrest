import validictory
from validictory.validator import DEFAULT_FORMAT_VALIDATORS

def number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

CONVERSION = {
    "integer": lambda s: int(s),
    "number": number,
    "boolean": lambda s: True if s.lower() == "true" else False,
    "array": lambda s: s.split(","),
}


def nullable_string(validator, fieldname, value, format_option):
    if value is None or not isinstance(value, basestring):
        raise ValueError("The value '{0}' of '{1}' is not null or a string"
            .format(value, fieldname))


FORMAT_VALIDATORS = {
    "nullableString": nullable_string
}
FORMAT_VALIDATORS.update(DEFAULT_FORMAT_VALIDATORS)


def validate_schema(request, schema):
    # validate schema
    query_schema = schema.get("query")
    if query_schema is not None:
        try:
            # Because all GET-Parameters are strings try to convert them
            # into the format specified in the schema
            params = {}
            for k in request.GET:
                params[k] = request.GET[k]
            for prop, o in query_schema.get('properties').iteritems():
                stype = o.get('type')
                if stype in CONVERSION:
                    converter = CONVERSION[stype]
                    v = params.get(prop)
                    if v is not None:
                        params[prop] = converter(v)
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
