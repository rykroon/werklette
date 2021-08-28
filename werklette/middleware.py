from werkzeug.exceptions import HTTPException, InternalServerError


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
    def __init__(self, app):
        self.app = app

    def __call__(self, request):
        try:
            return self.app(request)

        except Exception as e:
            raise InternalServerError(original_exception=e)

