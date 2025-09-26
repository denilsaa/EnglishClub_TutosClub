from django.db import models
from apps.estudiantes.models.estudiante import Estudiante
from apps.cursos.models.curso import Curso
from apps.cursos.models.asignatura import Asignatura
from apps.usuarios.models.usuario import Usuario

class Nota(models.Model):
    estudiante      = models.ForeignKey(Estudiante,   on_delete=models.CASCADE)
    curso           = models.ForeignKey(Curso,        on_delete=models.CASCADE)
    asignatura      = models.ForeignKey(Asignatura,   on_delete=models.CASCADE)
    fecha           = models.DateField()
    tipo_evaluacion = models.CharField(
        max_length=20,
        choices=[
            ('participacion', 'Participación'),
            ('oral',          'Oral'),
            ('tarea',         'Tarea'),
            ('mensual',       'Mensual'),
            ('final',         'Final'),
        ]
    )
    nota            = models.DecimalField(max_digits=5, decimal_places=2)
    observacion     = models.CharField(max_length=255, blank=True)
    gestion         = models.CharField(max_length=10)
    registrado_por  = models.ForeignKey(Usuario,      on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.estudiante} – {self.asignatura} ({self.tipo_evaluacion}): {self.nota}"
