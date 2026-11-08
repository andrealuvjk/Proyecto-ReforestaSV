# usuarios/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied

def rol_requerido(*roles_permitidos):
    """
    Decorador que restringe el acceso a la vista solo a los roles indicados.
    Ejemplo: @rol_requerido('ADMIN', 'RESPONSABLE')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied  # Redirige a pantalla de error HTTP 403
        return _wrapped_view
    return decorator