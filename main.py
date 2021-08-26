from werkzeug.wrappers import Response

from application import App

app = App()


@app.get('/')
def homepage(request):
    return Response('Hello World', content_type='plain/text')





