# apps/usuarios/forms/administrativo.py
from django import forms
from django.core.exceptions import ValidationError
from apps.usuarios.models import PersonalAdministrativo

class AdministrativoCuentaForm(forms.Form):
    username = forms.CharField(max_length=50, label="Usuario")
    # CharField para permitir cualquier string como "salt"
    correo = forms.CharField(max_length=120, label="Correo / Salt")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repetir Contraseña")

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("password2"):
            raise ValidationError("Las contraseñas no coinciden.")
        # normaliza espacios
        if data.get("correo"):
            data["correo"] = data["correo"].strip()
        return data


class AdministrativoDatosForm(forms.ModelForm):
    class Meta:
        model = PersonalAdministrativo
        fields = [
            'rol', 'nombres', 'apellidos', 'ci',
            'direccion', 'telefono', 'fecha_nacimiento',
            'archivo_documentacion', 'activo'
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }

    # Si quieres que el archivo sea obligatorio, deja este clean_*.
    # Si deseas que sea opcional, elimina la validación "if not f: ..."
    def clean_archivo_documentacion(self):
        f = self.cleaned_data.get("archivo_documentacion")
        if not f:
            raise forms.ValidationError("Este archivo es obligatorio.")
        if f.size > 5 * 1024 * 1024:  # 5 MB
            raise forms.ValidationError("El archivo no debe exceder los 5 MB.")
        return f
