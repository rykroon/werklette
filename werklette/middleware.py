import traceback
from werkzeug.exceptions import HTTPException, InternalServerError
from werklette.responses import Response


class Middleware:

    def __init__(self):
        ...


    def __call__(self, request):
        ...


class RoutingMiddleware:
    """
        Converts a Router into Middleware.
    """

    def __init__(self, router):
        self.router = router

    def __call__(self, request):
        adapter = self.router.bind_to_environ(request.environ)
        func, kwargs = adapter.match(path_info=request.path, method=request.method)
        request.set_path_params(kwargs)
        return func(request)


class ExceptionMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, request):
        try:
            return self.app(request)
        
        except HTTPException as e:
            return e


class ServerErrorMiddleware:
    def __init__(self, app, handler=None, debug=False):
        self.app = app
        self.handler = handler
        self.debug = debug

    def __call__(self, request):
        try:
            return self.app(request)

        except Exception as e:
            if self.debug:
                content = traceback.format_exception(type(e), e, e.__traceback__)
                return Response(content, status=500)

            if self.handler:
                return self.handler(request)

            return InternalServerError(original_exception=e)

