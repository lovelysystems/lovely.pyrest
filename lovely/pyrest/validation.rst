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

