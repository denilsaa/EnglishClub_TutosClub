# apps/usuarios/urls.py
from django.urls import path

from .views.login import login_view, logout_view
from .views.paneles import (
    panel_estudiante, panel_docente, panel_secretaria, panel_padre, panel_directivo
)
from .views.registro_estudiantes import registrar_regular, registrar_tecnico
from .views.registro_administrativo import registrar_administrativo

app_name = 'usuarios'

urlpatterns = [
    path('login/',  login_view,  name='login'),
    path('logout/', logout_view, name='logout'),

    path('panel/estudiante/',  panel_estudiante,  name='panel_estudiante'),
    path('panel/docente/',     panel_docente,     name='panel_docente'),
    path('panel/secretaria/',  panel_secretaria,  name='panel_secretaria'),
    path('panel/padre/',       panel_padre,       name='panel_padre'),
    path('panel/directivo/',   panel_directivo,   name='panel_directivo'),

    path('estudiantes/registrar/regular/', registrar_regular, name='registrar_regular'),
    path('estudiantes/registrar/tecnico/', registrar_tecnico, name='registrar_tecnico'),

    path('personal/registrar/', registrar_administrativo, name='registrar_administrativo'),
]
