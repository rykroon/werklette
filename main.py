from werklette import Werklette
from werklette.responses import JsonResponse
from werklette.routing import Router, Route


app = Werklette()


@app.get('/')
def homepage(request):
    return JsonResponse({'Hello': 'World'})


# A Router can be a stand-alone WSGI App.
router = Router([
    Route('/', endpoint=homepage, methods=['GET'])
])

