import validictory
import copy


class ValidationException(Exception):
    """A validation exception"""


class Validator(validictory.SchemaValidator):
    """Extend the validator
    """

    custom_validators = {}

    @staticmethod
    def register_custom_validator(name, func):
        Validator.custom_validators[name] = func

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

    def validate_custom_validator(self, x, fieldname, schema, props=None):
        """Allows to validate against custom validator.

        The given schema might define a custom validator for a field by
        passing 'custom_validator'. The used validator has to be registered by
        the static method 'register_custom_validator'.
        """
        validator = Validator.custom_validators.get(props)
        if not validator:
            raise validictory.SchemaError(
                "Custom validator %r not found" % props)
        value = x.get(fieldname)
        if not validator(value):
            self._error("Value %(value)r for field '%(fieldname)s' is not "
                        "valid due to custom validator %(validator)r",
                        value, fieldname, validator=props)


def custom_validator(name):
    """Decorator to register a custom validator
    """
    def f(func):
        Validator.register_custom_validator(name, func)
        return func
    return f


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
}


def _convert(kwargs, schema):
    params = copy.deepcopy(kwargs)
    for prop, o in schema.get('properties').items():
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
            except ValueError as error:
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
    for v in list(s["properties"].values()):
        v['required'] = False
    return s
