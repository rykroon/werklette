import traceback
from werkzeug.exceptions import HTTPException, InternalServerError
from werklette.responses import Response


class ExceptionMiddleware:

    def __init__(self, app, handlers: dict = {}):
        self.app = app
        # By default, there is an HTTPException handler that just returns 
        # the Exception. 
        self.handlers = {
            HTTPException: lambda req, exc: exc
        }
        self.handlers.update(handlers)

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
                return cls
        return None


class ServerErrorMiddleware:

    def __init__(self, app, handler=None, debug=False):
        self.app = app
        self.handler = handler
        self.debug = debug

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)

        except Exception as e:
            if self.debug:
                content = traceback.format_exception(type(e), e, e.__traceback__)
                return Response(content, status=500)

            if self.handler:
                request = environ.get('werkzeug.request')
                return self.handler(request)

            return InternalServerError(original_exception=e)

