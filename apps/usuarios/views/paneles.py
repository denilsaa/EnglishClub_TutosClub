# apps/usuarios/views/paneles.py
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache, cache_control

# ---------------------------
# Helpers de seguridad/SESION
# ---------------------------

def _require_session(request):
    """
    Si no hay sesión activa (usuario_id), redirige al login con namespace.
    Úselo al inicio de cada vista de panel.
    """
    if not request.session.get("usuario_id"):
        return redirect("usuarios:login")  # <-- namespace correcto
    return None


def _contexto_base(request):
    """
    Devuelve datos mínimos para las plantillas de panel.
    """
    return {
        "usuario_id": request.session.get("usuario_id"),
        "username": request.session.get("username"),
        "rol": request.session.get("rol"),
    }


# Decorador de no-cache para paneles
def _nocache(view_func):
    @never_cache
    @cache_control(no_store=True, no_cache=True, must_revalidate=True)
    def _wrapped(request, *args, **kwargs):
        r = _require_session(request)
        if r:
            return r
        return view_func(request, *args, **kwargs)
    return _wrapped


# ---------------------------
# VISTAS DE PANELES
# ---------------------------

@_nocache
def panel_directivo(request):
    """
    Panel para rol 'directivo'
    Template: templates/paneles/panel_directivo.html
    """
    ctx = _contexto_base(request)
    return render(request, "paneles/panel_directivo.html", ctx)


@_nocache
def panel_secretaria(request):
    """
    Panel para rol 'secretaria'
    Template: templates/paneles/panel_secretaria.html
    """
    ctx = _contexto_base(request)
    return render(request, "paneles/panel_secretaria.html", ctx)


@_nocache
def panel_docente(request):
    """
    Panel para rol 'docente'
    Template: templates/paneles/panel_docente.html
    """
    ctx = _contexto_base(request)
    return render(request, "paneles/panel_docente.html", ctx)


@_nocache
def panel_padre(request):
    """
    Panel para rol 'padre'
    Template: templates/paneles/panel_padre.html
    """
    ctx = _contexto_base(request)
    return render(request, "paneles/panel_padre.html", ctx)


@_nocache
def panel_estudiante(request):
    """
    Panel para rol 'estudiante'
    Template: templates/paneles/panel_estudiante.html
    """
    ctx = _contexto_base(request)
    return render(request, "paneles/panel_estudiante.html", ctx)
