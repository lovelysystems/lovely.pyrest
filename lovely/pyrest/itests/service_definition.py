# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH

from lovely.pyrest.service import Service

# This module contains several service definitions with
# predicates and validators for integration testing


# Define a simple service
service = Service('myService', '/service')


@service.get()
def get(request):
    return {'test': 'succeed'}


# Define a more complex service with validators
# and predicates
user = Service('user', '/user')


@user.get(accept='application/json',
          content_type='application/json')
def get_user(request):
    return {'test': 'succeed'}


schema = {
    "query": {
        "type": "object",
        "properties": {
            "u": {
                "type": "string",
                "format": "url"
            }
        }
    },
    "body": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            }
        }
    }
}


@user.post(schema=schema)
def post(request):
    return {'post_test': 'succeeded'}
