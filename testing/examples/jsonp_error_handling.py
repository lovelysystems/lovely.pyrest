from lovely.pyrest.service import Service
"""
To show the different error handling in the following example,
a request should have set the query parameter 'callback=your_callback' only.
Therefore, the request does not fullfil all required parameters specificed by
the schema below and a validation error occures.

The response could then look similar as follows:
Response: 200 OK
Content-Type: application/javascript; charset=UTF-8
your_callback({"status": "error", "errors": [{"location": "query", "description": "Required field 'id' is missing"}], "http_status": 400})
"""

svc_error = Service(name="svc_error", path='/svc/error')


schema = {
    "query": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string"
            }
        }
    }
}

@svc_error.get(schema=schema)
def get(request):
    return {'title': 'Hello World!'}
