from django.urls import path
from .views.login import login_view, logout_view
from .views.paneles import (
    panel_estudiante, panel_docente, panel_secretaria, panel_padre, panel_directivo
)
from .views.registro_estudiantes import (
    registrar_regular, registrar_tecnico
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

    # Registro de estudiantes (solo directivo/secretaria)
    path('estudiantes/registrar/regular/', registrar_regular, name='registrar_regular'),
    path('estudiantes/registrar/tecnico/', registrar_tecnico, name='registrar_tecnico'),
]
