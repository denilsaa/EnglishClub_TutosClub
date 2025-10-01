from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache, cache_control

def require_session(view):
    def _wrap(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        response = view(request, *args, **kwargs)
        return response
    return _wrap

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_session
def panel_estudiante(request):
    return render(request, 'paneles/panel_estudiante.html', {'username': request.session.get('username')})

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_session
def panel_docente(request):
    return render(request, 'paneles/panel_docente.html', {'username': request.session.get('username')})

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_session
def panel_secretaria(request):
    return render(request, 'paneles/panel_secretaria.html', {'username': request.session.get('username')})

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_session
def panel_padre(request):
    return render(request, 'paneles/panel_padre.html', {'username': request.session.get('username')})

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@require_session
def panel_directivo(request):
    return render(request, 'paneles/panel_directivo.html', {'username': request.session.get('username')})
