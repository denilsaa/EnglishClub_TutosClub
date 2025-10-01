from django import forms
from datetime import date

# Datos del padre
class PadreForm(forms.Form):
    nombres = forms.CharField(max_length=150)
    apellidos = forms.CharField(max_length=150)
    ci = forms.CharField(max_length=30)
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=30, required=False)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# Datos comunes del estudiante
class EstudianteBaseForm(forms.Form):
    nombres = forms.CharField(max_length=150)
    apellidos = forms.CharField(max_length=150)
    ci = forms.CharField(max_length=30)
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=30, required=False)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# Regular: escolar + grupo
class EstudianteRegularForm(EstudianteBaseForm):
    colegio_universidad = forms.CharField(label="Colegio", max_length=150)
    grupo = forms.ChoiceField(choices=[('Sweet','Sweet'),('Smart','Smart'),('Teens','Teens')])

# Técnico: universidad/ocupación
class EstudianteTecnicoForm(EstudianteBaseForm):
    colegio_universidad = forms.CharField(label="Universidad/Instituto", max_length=150, required=False)
    ocupacion = forms.CharField(max_length=120, required=False)

# Credenciales (para padre en REGULAR, para estudiante en TÉCNICO)
class CuentaForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=150)
    contrasena = forms.CharField(widget=forms.PasswordInput)
    contrasena2 = forms.CharField(widget=forms.PasswordInput, label="Repite la contraseña")

    def clean(self):
        data = super().clean()
        if data.get('contrasena') != data.get('contrasena2'):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return data
