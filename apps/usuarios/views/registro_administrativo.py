# apps/usuarios/views/registro_administrativo.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_control

from ..forms.administrativo import AdministrativoCuentaForm, AdministrativoDatosForm
from ..utils.crypto import hash_password
from apps.usuarios.models import Usuario, PersonalAdministrativo

def _require_directivo(request):
    """Devuelve None si OK; si no, retorna redirect al login/panel correcto."""
    usuario_id = request.session.get("usuario_id")
    rol = request.session.get("rol")
    if not usuario_id:
        return redirect("usuarios:login")
    if rol != "directivo":
        messages.error(request, "Acceso restringido: solo Directivo.")
        # redirige al panel del rol de la sesión
        destino = {
            "secretaria": "usuarios:panel_secretaria",
            "docente": "usuarios:panel_docente",
            "padre": "usuarios:panel_padre",
            "estudiante": "usuarios:panel_estudiante",
            "directivo": "usuarios:panel_directivo",
        }.get(rol, "usuarios:login")
        return redirect(destino)
    return None


@never_cache
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def registrar_administrativo(request):
    # Bloqueo por rol
    gate = _require_directivo(request)
    if gate:
        return gate

    cancel_url = reverse("usuarios:panel_directivo")

    if request.method == "POST":
        f_cuenta = AdministrativoCuentaForm(request.POST, prefix="cuenta")
        f_datos = AdministrativoDatosForm(request.POST, request.FILES, prefix="adm")

        if f_cuenta.is_valid() and f_datos.is_valid():
            username = f_cuenta.cleaned_data["username"]
            correo = f_cuenta.cleaned_data["correo"]
            passwd = f_cuenta.cleaned_data["password"]

            # usuario ya existe
            if Usuario.objects.filter(nombre_usuario=username).exists():
                f_cuenta.add_error("username", "El usuario ya existe.")
            else:
                try:
                    # crear Usuario (sha256 + salt basado en 'correo/salt')
                    usuario = Usuario.objects.create(
                        nombre_usuario=username,
                        contrasena=hash_password(passwd, correo),
                        correo=correo
                    )

                    # crear PersonalAdministrativo
                    administrativo = f_datos.save(commit=False)
                    administrativo.usuario = usuario
                    administrativo.save()

                    messages.success(request, "Registro exitoso.")
                    return redirect("usuarios:panel_directivo")

                except Exception as e:
                    messages.error(request, f"Ocurrió un error al guardar: {e}")

        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            # Log útil en consola para depurar
            print("Errores (cuenta):", f_cuenta.errors)
            print("Errores (datos):", f_datos.errors)

    else:
        f_cuenta = AdministrativoCuentaForm(prefix="cuenta")
        f_datos = AdministrativoDatosForm(prefix="adm")

    return render(request, "registros/registro_administrativo.html", {
        "f_cuenta": f_cuenta,
        "f_datos": f_datos,
        "cancel_url": cancel_url
    })
