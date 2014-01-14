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


def validate(schema):
    """ A decorator to validate the kwargs of the decorated function against
    the given schema. The schema has to be a valid validictory schema
    """

    def wrapper(f):
        def validation_wrapper(*args, **kwargs):
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
