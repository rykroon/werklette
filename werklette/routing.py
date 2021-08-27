from werkzeug.routing import Map, Rule
from werklette.requests import Request


class Router(Map):
    def __call__(self, request):
        adapter = self.bind_to_environ(request.environ)
        func, kwargs = adapter.match(path_info=request.path, method=request.method)
        request._path_params = kwargs
        return func(request)


class Route(Rule):
    ...