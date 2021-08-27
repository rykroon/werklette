from werklette import Werklette
from werklette.responses import JsonResponse


app = Werklette()


@app.get('/')
def homepage(request):
    return JsonResponse({'Hello': 'World'})

