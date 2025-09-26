from django.db import models
from apps.usuarios.models.personal import PersonalAdministrativo
from datetime import date, timedelta

class Curso(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
    ]

    TIPOS_ESTUDIANTE = [
        ('tecnico', 'Técnico'),
        ('regular', 'Regular'),
    ]

    nombre = models.CharField(max_length=100)
    docente = models.ForeignKey(PersonalAdministrativo, on_delete=models.CASCADE)
    gestion = models.CharField(max_length=10)
    dias = models.CharField(max_length=150)  # p.ej. "Lunes,Miércoles,Viernes"
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo_estudiante = models.CharField(
        max_length=10, choices=TIPOS_ESTUDIANTE, default='regular'
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def dias_list(self) -> list[str]:
        """
        Retorna una lista con los días configurados, en minúsculas,
        p.ej. ['lunes', 'miércoles', 'viernes'].
        """
        if not self.dias:
            return []
        return [d.strip().lower() for d in self.dias.split(',')]

    def get_semestre_range(self) -> tuple[date, date]:
        """
        Devuelve una tupla (inicio, fin) del semestre actual:
        - Si el mes <= 6: 1 de enero a 30 de junio.
        - Si el mes > 6:  1 de julio a 31 de diciembre.
        """
        hoy = date.today()
        año = hoy.year
        if hoy.month <= 6:
            return date(año, 1, 1), date(año, 6, 30)
        return date(año, 7, 1), date(año, 12, 31)

    def fechas_semestre(self) -> list[date]:
        """
        Genera todas las fechas dentro del semestre actual cuyo
        weekday() coincida con uno de los días configurados.
        weekday(): 0=lunes ... 6=domingo.
        """
        inicio, fin = self.get_semestre_range()

        # Mapeo de nombre en español a weekday()
        mapa = {
            'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2,
            'jueves': 3, 'viernes': 4, 'sábado': 5, 'sabado': 5,
            'domingo': 6
        }
        dias_permitidos = [mapa[d] for d in self.dias_list() if d in mapa]

        fechas = []
        actual = inicio
        while actual <= fin:
            if actual.weekday() in dias_permitidos:
                fechas.append(actual)
            actual += timedelta(days=1)
        return fechas
