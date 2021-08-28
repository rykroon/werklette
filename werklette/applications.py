from werklette.routing import Router, Route
from werklette.requests import Request
from werklette.middleware import ExceptionMiddleware, RoutingMiddleware, ServerErrorMiddleware


class Werklette:
    def __init__(self, debug=False, routes=None, middleware=None):
        self.debug = debug
        self.middleware = middleware
        self.router = Router(routes)

    def __call__(self, environ, start_response):
        request = Request(environ)
        app = RoutingMiddleware(self.router)
        app = ExceptionMiddleware(app)
        app = ServerErrorMiddleware(app, debug=self.debug)
        response = app(request)
        return response(environ, start_response)

    def route(self, url, methods=None):
        def decorator(func):
            route = Route(url, endpoint=func, methods=methods)
            self.router.add(route)
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


