from django.urls import path
from apps.usuarios.views.login import login_view  # Importar desde login.py

urlpatterns = [
    path('login/', login_view, name='login'),  # Ruta para el login
]
