from werkzeug.datastructures import ImmutableDict
from werkzeug.routing import Map, Rule


class Router(Map):

    def __call__(self, request):
        adapter = self.bind_to_environ(request.environ)
        func, kwargs = adapter.match(path_info=request.path, method=request.method)
        request._path_params = ImmutableDict(kwargs)
        return func(request)


class Route(Rule):
    ...