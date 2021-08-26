from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request


class App:
    def __init__(self, routes=None, middleware=None):
        self.middleware = middleware
        self.url_map = Map(routes)

    @Request.application
    def __call__(self, request):
        return self.dispatch(request)

    def dispatch(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        func, kwargs = adapter.match(path_info=request.path, method=request.method)
        request.query_params = request.args
        request.path_params = kwargs
        return func(request)

    def route(self, url, methods=None):
        def decorator(func):
            rule = Rule(url, endpoint=func, methods=methods)
            self.url_map.add(rule)
            return func
        return decorator

    def get(self, url):
        return self.route(url, methods=['GET'])

    def post(self, url):
        return self.route(url, methods=['POST'])

    def put(self, url):
        return self.route(url, methods=['PUT'])

    def delete(self, url):
        return self.route(url, methods=['DELETE'])


