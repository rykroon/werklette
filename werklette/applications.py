from werklette.routing import Router, Route
from werklette.requests import Request
from werklette.middleware import ExceptionMiddleware, ServerErrorMiddleware


class Werklette:
    def __init__(self, debug=False, routes=None, middleware=None, exception_handlers=None):
        self.debug = debug
        self.router = Router(routes)
        self.middleware = [] if middleware is None else list(middleware)
        self.exception_handlers = {} if exception_handlers is None else dict(exception_handlers)
        
    def __call__(self, environ, start_response):
        Request(environ)
        app = self.router
        app = ExceptionMiddleware(app)
        for cls, options in self.middleware:
            app = cls(app, **options)
        app = ServerErrorMiddleware(app, debug=self.debug)
        response = app(environ, start_response)
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


