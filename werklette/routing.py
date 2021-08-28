from werkzeug.routing import Map, Rule
from werklette.requests import Request


class Router(Map):

    def __call__(self, environ, start_response):
        request = Request(environ)
        adapter = self.bind_to_environ(request.environ)
        func, kwargs = adapter.match(path_info=request.path, method=request.method)
        request.set_path_params(kwargs)
        return func(request)(environ, start_response)


class Route(Rule):
    ...