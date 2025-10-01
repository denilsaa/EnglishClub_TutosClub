# apps/usuarios/urls.py
from django.urls import path
from .views.login import login_view, logout_view
from .views.paneles import (
    panel_estudiante, panel_docente, panel_secretaria, panel_padre, panel_directivo
)

urlpatterns = [
    path('login/',  login_view,  name='login'),
    path('logout/', logout_view, name='logout'),

    # Paneles
    path('panel/estudiante/',  panel_estudiante,  name='panel_estudiante'),
    path('panel/docente/',     panel_docente,     name='panel_docente'),
    path('panel/secretaria/',  panel_secretaria,  name='panel_secretaria'),
    path('panel/padre/',       panel_padre,       name='panel_padre'),
    path('panel/directivo/',   panel_directivo,   name='panel_directivo'),
]
