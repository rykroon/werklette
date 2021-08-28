from werkzeug.exceptions import HTTPException, InternalServerError


class Middleware:

    def __init__(self):
        ...


    def __call__(self, request):
        ...


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

