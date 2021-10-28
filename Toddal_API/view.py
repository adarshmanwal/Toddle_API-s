from django.http import HttpResponse


def index(request):
    return HttpResponse('''
    <h1>Toddle Backend Task (Virtual Classroom)</h1>
    <p>Simple stateless microservice with following API endpoints.</p>

    <p>Github link: <a href="https://github.com/adarshmanwal/Toddle_API-s" target="_blank">https://github.com/adarshmanwal/Toddle_API-s</a></p>
    <p>Documentation: <a href="https://github.com/adarshmanwal/Toddle_API-s/blob/master/README.md" target="_blank">https://github.com/adarshmanwal/Toddle_API-s/blob/master/README.md</a></p>
    ''')