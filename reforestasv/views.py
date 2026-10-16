from django.http import HttpResponse

def inicio(request):
    return HttpResponse("<h1>¡Servidor de ReforestaSV funcionando correctamente!</h1>")

# Create your views here.
