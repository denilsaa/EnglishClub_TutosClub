from django.shortcuts import redirect

class PanelAuthMiddleware:
    """
    Bloquea cualquier acceso a /usuarios/panel/... si no hay sesión (usuario_id).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or ""
        if path.startswith("/usuarios/panel/") and not request.session.get("usuario_id"):
            return redirect("login")
        return self.get_response(request)
