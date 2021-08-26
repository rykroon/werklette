import json
from werkzeug.wrappers import Response


class JsonResponse(Response):

    def __init__(self, content, **kwargs):
        content = json.dumps(content)
        super().__init__(content, content_type='application/json', **kwargs)