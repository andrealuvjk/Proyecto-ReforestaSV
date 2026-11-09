from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('inventarios/')  # Cambia 'dashboard' por la ruta a donde va un usuario logeado
    return redirect('login')