from werkzeug.wrappers import Response

from app import App

app = App()


@app.get('/')
def homepage(request):
    return Response('Hello World', content_type='plain/text')





