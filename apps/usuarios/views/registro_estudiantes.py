# apps/usuarios/views/registro_estudiantes.py
import hashlib, secrets
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.usuarios.forms.estudiantes import (
    PadreForm, EstudianteRegularForm, EstudianteTecnicoForm, CuentaForm
)
from apps.usuarios.models import Usuario, Padre
from apps.estudiantes.models import Estudiante


# ---------------- Helpers ----------------

def requiere_directivo_o_secretaria(view):
    """
    Permite el acceso solo si el rol en la sesión es 'directivo' o 'secretaria'.
    """
    def _wrap(request, *args, **kwargs):
        rol = request.session.get('rol')
        if rol not in ('directivo', 'secretaria'):
            messages.error(request, "No tienes permisos para registrar estudiantes.")
            return redirect('login')
        return view(request, *args, **kwargs)
    return _wrap


def crear_usuario(nombre_usuario: str, contrasena_plana: str) -> Usuario:
    """
    Crea Usuario usando tu esquema (sha256(password + salt)) guardando el salt en 'correo'.
    Lanza ValueError si el nombre_usuario ya existe.
    """
    if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
        raise ValueError("El nombre de usuario ya existe.")

    salt = secrets.token_hex(8)
    hashpass = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

    return Usuario.objects.create(
        nombre_usuario=nombre_usuario,
        contrasena=hashpass,
        correo=salt  
    )


# ---------------- Registro REGULAR (menor; credenciales para el Padre) ----------------

@requiere_directivo_o_secretaria
def registrar_regular(request):
    cancel_url = reverse('panel_secretaria') if request.session.get('rol') == 'secretaria' else reverse('panel_directivo')

    if request.method == 'POST':
        padre_form  = PadreForm(request.POST, prefix='padre')
        est_form    = EstudianteRegularForm(request.POST, prefix='est')
        cuenta_form = CuentaForm(request.POST, prefix='cuenta')

        if padre_form.is_valid() and est_form.is_valid() and cuenta_form.is_valid():
            try:
                u_padre = crear_usuario(
                    cuenta_form.cleaned_data['nombre_usuario'],
                    cuenta_form.cleaned_data['contrasena']
                )
            except ValueError as e:
                messages.error(request, str(e))
                return render(request, 'registros/registro_regular.html', {
                    'padre_form': padre_form,
                    'est_form': est_form,
                    'cuenta_form': cuenta_form,
                    'cancel_url': cancel_url,
                })

            padre = Padre.objects.create(usuario=u_padre, **padre_form.cleaned_data)

            est_data = est_form.cleaned_data
            Estudiante.objects.create(
                usuario=u_padre,
                nombres=est_data['nombres'],
                apellidos=est_data['apellidos'],
                ci=est_data['ci'],
                direccion=est_data.get('direccion', ''),
                telefono=est_data.get('telefono', ''),
                fecha_nacimiento=est_data['fecha_nacimiento'],
                tipo='regular',
                grupo=est_data['grupo'],
                colegio_universidad=est_data['colegio_universidad'],
                ocupacion='Estudiante',
                padre=padre
            )

            messages.success(request, "Estudiante REGULAR registrado. Usuario y contraseña asignados al PADRE.")
            return redirect('panel_secretaria' if request.session.get('rol') == 'secretaria' else 'panel_directivo')

    else:
        padre_form  = PadreForm(prefix='padre')
        est_form    = EstudianteRegularForm(prefix='est')
        cuenta_form = CuentaForm(prefix='cuenta')

    return render(request, 'registros/registro_regular.html', {
        'padre_form': padre_form,
        'est_form': est_form,
        'cuenta_form': cuenta_form,
        'cancel_url': cancel_url,
    })


@requiere_directivo_o_secretaria
def registrar_tecnico(request):
    cancel_url = reverse('panel_secretaria') if request.session.get('rol') == 'secretaria' else reverse('panel_directivo')

    if request.method == 'POST':
        est_form    = EstudianteTecnicoForm(request.POST, prefix='est')
        cuenta_form = CuentaForm(request.POST, prefix='cuenta')

        if est_form.is_valid() and cuenta_form.is_valid():
            try:
                u_est = crear_usuario(
                    cuenta_form.cleaned_data['nombre_usuario'],
                    cuenta_form.cleaned_data['contrasena']
                )
            except ValueError as e:
                messages.error(request, str(e))
                return render(request, 'registros/registro_tecnico.html', {
                    'est_form': est_form,
                    'cuenta_form': cuenta_form,
                    'cancel_url': cancel_url,
                })

            ed = est_form.cleaned_data
            Estudiante.objects.create(
                usuario=u_est,
                nombres=ed['nombres'],
                apellidos=ed['apellidos'],
                ci=ed['ci'],
                direccion=ed.get('direccion', ''),
                telefono=ed.get('telefono', ''),
                fecha_nacimiento=ed['fecha_nacimiento'],
                tipo='tecnico',
                grupo=None,
                colegio_universidad=ed.get('colegio_universidad', ''),
                ocupacion=ed.get('ocupacion', '')
            )

            messages.success(request, "Estudiante TÉCNICO registrado. Usuario y contraseña asignados al ESTUDIANTE.")
            return redirect('panel_secretaria' if request.session.get('rol') == 'secretaria' else 'panel_directivo')

    else:
        est_form    = EstudianteTecnicoForm(prefix='est')
        cuenta_form = CuentaForm(prefix='cuenta')

    return render(request, 'registros/registro_tecnico.html', {
        'est_form': est_form,
        'cuenta_form': cuenta_form,
        'cancel_url': cancel_url,
    })