==========
Validation
==========

This documentation is about validating keyword arguments passed to functions or
methods. The validation is done by a decorator with using a given schema. The
actual validation is done by `validictory <https://github.com/sunlightlabs/validictory>`_.
For details about the schema definitions see `json-schema-validation <http://json-schema.org/latest/json-schema-validation.html>`_

The `validate` decorator
========================

The decorator `validate` requires a schema passed to the decorator. Let's
define a schema for keyword arguments like data={"a":"foo", "b":42}::

    >>> schema = {
    ...     "type": "object",
    ...     "properties": {
    ...         "data": {
    ...             "type": "object",
    ...             "properties": {
    ...                 "a": {"type":"string"},
    ...                 "b": {"type":"integer"},
    ...             }
    ...         }
    ...     }
    ... }

Now implement a function to decorate with the required signature::

    >>> from lovely.pyrest.validation import validate

    >>> @validate(schema)
    ... def sample(data):
    ...     pass

If the function get called with valid keyword arguments everything is fine::

    >>> sample(data={"a":"foo", "b":42})

If the given keyword arguments are not valid a ValidationException is raised::

    >>> sample(data="bar")
    Traceback (most recent call last):
    ValidationException: Value 'bar' for field 'data' is not of type object


Get conversion
==============

Requests with get params always lead to strings. Nevertheless using the optional
'convert_get_params' param will try to convert to the correct type. This works as
get params are always in a flat structure, e.g. no sub objects.

Prepare a flat schema::

    >>> schema = {
    ...     "type": "object",
    ...     "properties": {
    ...         "a": {"type":"string", "required": False},
    ...         "b": {"type":"integer", "required": False},
    ...         "c": {"type":"number", "required": False},
    ...         "d": {"type":"boolean", "required": False},
    ...     }
    ... }

    >>> @validate(schema, convert_get_params=True)
    ... def sample_get(a="string", b=1, c=1.1, d=False):
    ...     return a, b, c, d

Use valid values, the converted values will be used in the function::

    >>> sample_get(a="foo",
    ...            b="42",
    ...            c="3.14159265359",
    ...            d="true")
    ('foo', 42, 3.14159265359, True)

Using a non integer value for integer properties will raise a validation
exception::

    >>> sample_get(b="a string")
    Traceback (most recent call last):
    ValidationException: Value 'a string' for field 'b' is not of type integer

Also floats are not allowed on integer properties::

    >>> sample_get(b="17.4")
    Traceback (most recent call last):
    ValidationException: Value '17.4' for field 'b' is not of type integer

String values are not allowed for number properties::

    >>> sample_get(c="a string")
    Traceback (most recent call last):
    ValidationException: Value 'a string' for field 'c' is not of type number

Integer values are allowed for number properties:

    >>> sample_get(c="8086")
    ('string', 1, 8086, False)

Boolean properties return True if the word true is entered in any case::

    >>> sample_get(d="trUe")
    ('string', 1, 1.1, True)

Boolean properties return False if the word false is entered in any case::

    >>> sample_get(d="falSE")
    ('string', 1, 1.1, False)

Any other value is not allowed on boolean properties::

    >>> sample_get(d="None")
    Traceback (most recent call last):
    ValidationException: Value 'None' for field 'd' is not of type boolean

Custom validators
=================

It's possible to define custom validators within a validations schema::

    >>> schema = {
    ...     "type": "object",
    ...     "properties": {
    ...         "data": {
    ...             "custom_validator": "x"
    ...         }
    ...     }
    ... }

The implementation of a custom validator has to return boolean True to
validate the given value. The validator will get the field value as parameter::

    >>> from lovely.pyrest.validation import custom_validator

    >>> @custom_validator("x")
    ... def custom_validator(value):
    ...     return value == 'pass'

Now lets validate against the failing schema::

    >>> @validate(schema)
    ... def sample(data):
    ...     pass

    >>> sample(data="fail")
    Traceback (most recent call last):
    ValidationException: Value 'fail' for field 'data' is not valid due to custom validator 'x'

Now lets validate agains a passing schema::

    >>> sample(data="pass")

If the given custom_validator is not registered a SchemaError is raised::

    >>> schema = {
    ...     "type": "object",
    ...     "properties": {
    ...         "data": {
    ...             "custom_validator": "z"
    ...         }
    ...     }
    ... }

    >>> @validate(schema)
    ... def sample(data):
    ...     pass

    >>> sample(data="blah")
    Traceback (most recent call last):
    ValidationException: Custom validator 'z' not found
