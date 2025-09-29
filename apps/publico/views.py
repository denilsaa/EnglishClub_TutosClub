# apps/publico/views.py 
from django.shortcuts import render 
def login_view(request): 
    return render(request, 'publico/registro_estudiante.html')