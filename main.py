from werkzeug.exceptions import HTTPException
from werklette import Werklette
from werklette.responses import JsonResponse
from werklette.routing import Router, Route


def http_exception_handler(req, exc):
    return JsonResponse({
        'error': exc.name,
        'error_description': exc.description
    }, status=exc.code)


exception_handlers = {
    HTTPException: http_exception_handler
}

app = Werklette(debug=True, exception_handlers=exception_handlers)


@app.get('/')
def homepage(request):
    return JsonResponse({'Hello': 'World'})


# A Router can be a stand-alone WSGI App.
router = Router([
    Route('/', endpoint=homepage, methods=['GET'])
])

