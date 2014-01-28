import validictory
import copy


class ValidationException(Exception):
    """A validation exception"""


class Validator(validictory.SchemaValidator):
    """Extend the validator
    """

    def validate_oneOf(self, x, fieldname, schema, props=None):
        """Allows to provide multiple schemas for one property

        If the validation fails the error from the last validation is raised.
        """
        data = x[fieldname]
        error = None
        for s in props:
            try:
                self.validate(data, s)
                return
            except validictory.FieldValidationError as e:
                error = e
        if error:
            raise error


def _number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def _boolean(s):
    b = s.lower()
    if b == "true":
        return True
    elif b == "false":
        return False
    raise ValueError

_CONVERSION = {
    "integer": lambda s: int(s),
    "number": _number,
    "boolean": _boolean,
    "array": lambda s: s.split(","),
}


def _convert(kwargs, schema):
    params = copy.deepcopy(kwargs)
    for prop, o in schema.get('properties').iteritems():
        stype = o.get('type')
        if stype in _CONVERSION:
            converter = _CONVERSION[stype]
            v = params.get(prop)
            if v is not None:
                try:
                    params[prop] = converter(v)
                except:
                    # do not convert - validation should fail
                    pass
    return params

def validate(schema, convert_get_params=False):
    """ A decorator to validate the kwargs of the decorated function against
    the given schema. The schema has to be a valid validictory schema.
    If flag 'convert_get_params' is set to True, the kwargs will be
    converted into the appropriate datatypes. Use this flag to validate
    get params correctly on a service.
    """

    def wrapper(f):
        def validation_wrapper(*args, **kwargs):
            if convert_get_params:
                kwargs = _convert(kwargs, schema)
            try:
                validictory.validate(kwargs, schema, Validator)
            except ValueError, error:
                raise ValidationException(error.message)
            return f(*args, **kwargs)
        # link doc with function docstring, so it's accessible for generating
        # documentation
        validation_wrapper.__doc__ = f.__doc__
        return validation_wrapper
    return wrapper


def non_required(schema):
    """ Helper function  to make all properties optional
    """
    s = copy.deepcopy(schema)
    for v in s["properties"].values():
        v['required'] = False
    return s
