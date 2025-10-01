# apps/usuarios/middleware.py
from django.shortcuts import redirect

class RequireSessionForPanelMiddleware:
    """
    Bloquea acceso a /usuarios/panel/... si no hay sesión.
    Use 'apps.usuarios.middleware.RequireSessionForPanelMiddleware' en settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/usuarios/panel/') and not request.session.get('usuario_id'):
            return redirect('usuarios:login')
        return self.get_response(request)


# Alias para compatibilidad con proyectos que esperan este nombre
class PanelAuthMiddleware(RequireSessionForPanelMiddleware):
    """
    Compatibilidad: mismo comportamiento que RequireSessionForPanelMiddleware,
    pero con el nombre que settings.py estaba esperando.
    """
    pass
