# apps/usuarios/views/login.py
import hashlib
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.usuarios.models import Usuario, PersonalAdministrativo, Padre
from apps.estudiantes.models import Estudiante
from django.views.decorators.cache import never_cache, cache_control

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # 1) Buscar usuario
        try:
            usuario = Usuario.objects.get(nombre_usuario=username)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('usuarios:login')  # Aquí también debe ser con el namespace

        # 2) Verificar contraseña
        def verificar_contrasena(plana: str, hash_stored: str) -> bool:
            salt = (usuario.correo or "").split('@')[0]
            hashed = hashlib.sha256((plana + salt).encode()).hexdigest()
            return hashed == hash_stored

        if not verificar_contrasena(password, usuario.contrasena):
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('usuarios:login')  # Aquí también debe ser con el namespace

        # 3) Resolver rol/panel
        destino = 'home'  # fallback si no se detecta perfil
        rol_str = 'desconocido'

        admin = PersonalAdministrativo.objects.filter(usuario=usuario).first()
        if admin:
            rol_str = admin.rol
            destino = {
                'directivo': 'usuarios:panel_directivo',
                'secretaria': 'usuarios:panel_secretaria',
                'docente': 'usuarios:panel_docente',
            }.get(admin.rol, 'home')
        elif Padre.objects.filter(usuario=usuario).exists():
            rol_str = 'padre'
            destino = 'usuarios:panel_padre'
        elif Estudiante.objects.filter(usuario=usuario).exists():
            rol_str = 'estudiante'
            destino = 'usuarios:panel_estudiante'

        # 4) Guardar sesión
        request.session['usuario_id'] = usuario.id
        request.session['username'] = usuario.nombre_usuario
        request.session['rol'] = rol_str

        # 5) Redirigir al panel
        return redirect(reverse(destino))

    return render(request, 'publico/login.html')

@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def logout_view(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('usuarios:login')  # Aquí también debe ser con el namespace
