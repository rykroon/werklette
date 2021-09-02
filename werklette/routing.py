from werkzeug.routing import Map, Rule
from werklette.requests import Request


class Router(Map):

    def __call__(self, environ, start_response):
        request = environ.get('werkzeug.request') or Request(environ)
        adapter = self.bind_to_environ(request.environ)
        endpoint, kwargs = adapter.match(path_info=request.path, method=request.method)
        request._set_path_params(kwargs)
        return endpoint(request)


class Route(Rule):
    ...