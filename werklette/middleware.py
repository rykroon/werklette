import traceback
from werkzeug.exceptions import HTTPException, InternalServerError
from werklette.responses import Response


class ExceptionMiddleware:

    def __init__(self, app, handlers: dict = {}, debug=False):
        self.app = app
        self.handlers = {
            HTTPException: lambda req, exc: exc,
            Exception: self.server_error_handler
        }
        self.handlers.update(handlers)
        self.debug = debug

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        
        except Exception as e:
            handler = None

            if isinstance(e, HTTPException):
                handler = self.handlers.get(e.code)
            
            if handler is None:
                handler = self.lookup_handler(e)

            if handler:
                request = environ.get('werkzeug.request')
                return handler(request, e)
                
            raise e

    def lookup_handler(self, exc):
        for cls in type(exc).__mro__:
            if cls in self.handlers:
                return self.handlers[cls]
        return None

    def server_error_handler(self, request, e):
        if self.debug:
            description = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            return InternalServerError(description=description)

        return InternalServerError(original_exception=e)

