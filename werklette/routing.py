from werkzeug.routing import Map, Rule
from werklette.requests import Request


class Router(Map):

    def __call__(self, environ, start_response):
        # If there isn't already a Request object that was made
        # then the router is the app.
        router_as_app = 'werkzeug.request' not in environ
        request = environ.get('werkzeug.request') or Request(environ)
        adapter = self.bind_to_environ(request.environ)
        endpoint, kwargs = adapter.match(path_info=request.path, method=request.method)
        request._set_path_params(kwargs)
        response = endpoint(request)
        if router_as_app:
            return response(environ, start_response)
        return response


class Route(Rule):
    ...