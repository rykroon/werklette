import json
from werkzeug.wrappers import Response as WerkzeugResponse


class Response(WerkzeugResponse):
    ...


class JsonResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, response: dict, **kwargs):
        response = json.dumps(response)
        super().__init__(response, **kwargs)