from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario, PersonalAdministrativo, Padre
from apps.estudiantes.models import Estudiante
import hashlib
import secrets
from datetime import date


class Command(BaseCommand):
    help = 'Crea datos demo de usuarios, personal administrativo, estudiantes y padres'

    def crear_usuario_admin(self, nombre_usuario, rol, nombres, apellidos, ci, direccion, telefono, fecha_nacimiento):
        if not Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
            contrasena_plana = 'admin123'
            salt = secrets.token_hex(8)
            contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

            usuario = Usuario.objects.create(
                nombre_usuario=nombre_usuario,
                contrasena=contrasena_hash,
                correo=salt  # guardamos salt en correo temporalmente
            )

            PersonalAdministrativo.objects.create(
                usuario=usuario,
                rol=rol,
                nombres=nombres,
                apellidos=apellidos,
                ci=ci,
                direccion=direccion,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento
            )

            self.stdout.write(f"✅ Usuario administrativo '{nombre_usuario}' creado con rol '{rol}' y contraseña: {contrasena_plana}")
        else:
            self.stdout.write(f"⚠️ El usuario administrativo '{nombre_usuario}' ya existe.")

    def crear_padre(self, nombre_usuario, nombres, apellidos, ci, direccion, telefono, fecha_nacimiento):
        # Primero crea el Usuario si no existe
        if not Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
            contrasena_plana = 'admin123'
            salt = secrets.token_hex(8)
            contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

            usuario = Usuario.objects.create(
                nombre_usuario=nombre_usuario,
                contrasena=contrasena_hash,
                correo=salt
            )
            self.stdout.write(f"✅ Usuario padre '{nombre_usuario}' creado, contraseña: {contrasena_plana}")
        else:
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
            self.stdout.write(f"⚠️ El usuario padre '{nombre_usuario}' ya existía.")

        # Luego crea el perfil Padre
        pad, created = Padre.objects.get_or_create(
            usuario=usuario,
            defaults={
                'nombres': nombres,
                'apellidos': apellidos,
                'ci': ci,
                'direccion': direccion,
                'telefono': telefono,
                'fecha_nacimiento': fecha_nacimiento,
            }
        )
        if created:
            self.stdout.write(f"✅ Perfil Padre para '{nombre_usuario}' creado.")
        else:
            self.stdout.write(f"⚠️ Perfil Padre para '{nombre_usuario}' ya existía.")

    def crear_estudiante(self, nombre_usuario, nombres, apellidos, ci, fecha_nacimiento, tipo_estudiante, padre_usuario=None):
        # 1) Usuario
        if not Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
            contrasena_plana = 'admin123'
            salt = secrets.token_hex(8)
            contrasena_hash = hashlib.sha256((contrasena_plana + salt).encode()).hexdigest()

            usuario = Usuario.objects.create(
                nombre_usuario=nombre_usuario,
                contrasena=contrasena_hash,
                correo=salt
            )
            self.stdout.write(f"✅ Usuario estudiante '{nombre_usuario}' creado como '{tipo_estudiante}', pwd: {contrasena_plana}")
        else:
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
            self.stdout.write(f"⚠️ El usuario estudiante '{nombre_usuario}' ya existía.")

        # 2) Obtén al padre si corresponde
        padre_obj = None
        if padre_usuario:
            try:
                padre_usr = Usuario.objects.get(nombre_usuario=padre_usuario)
                padre_obj = Padre.objects.get(usuario=padre_usr)
            except (Usuario.DoesNotExist, Padre.DoesNotExist):
                self.stdout.write(f"❌ No se encontró perfil Padre para usuario '{padre_usuario}'. Se creará sin padre.")

        # 3) Crear Estudiante
        est, created = Estudiante.objects.get_or_create(
            usuario=usuario,
            defaults={
                'nombres': nombres,
                'apellidos': apellidos,
                'ci': ci,
                'fecha_nacimiento': fecha_nacimiento,
                'tipo': tipo_estudiante,
                'padre': padre_obj
            }
        )
        if created:
            msg = f"✅ Estudiante '{nombre_usuario}' ({tipo_estudiante}) creado."
            if padre_obj:
                msg += f" Padre: {padre_usuario}"
            self.stdout.write(msg)
        else:
            self.stdout.write(f"⚠️ El estudiante '{nombre_usuario}' ya existía.")

    def handle(self, *args, **kwargs):
        self.stdout.write("🌟 Creando datos de prueba...")

        # Admins
        self.crear_usuario_admin('dadmin', 'directivo', 'Admin', 'Principal', '12345678', 'Av. Siempre Viva 123', '70000000', date(1990, 1, 1))
        self.crear_usuario_admin('secretaria1', 'secretaria', 'Ana', 'Lopez', '87654321', 'Calle Falsa 456', '70123456', date(1992, 5, 10))
        self.crear_usuario_admin('docente1', 'docente', 'Carlos', 'Martinez', '11223344', 'Av. Central 789', '70234567', date(1985, 7, 20))

        # Padre
        self.crear_padre('padre1', 'Jorge', 'Perez', '55667788', 'Calle Luna 123', '70345678', date(1975, 3, 15))

        # Estudiantes
        self.crear_estudiante('estudiante_tecnico1', 'Luis', 'Gomez', '99887766', date(2005, 9, 5), 'tecnico')

        # Asociamos el estudiante_regular1 con padre1
        self.crear_estudiante('estudiante_regular1', 'Maria', 'Fernandez', '88776655', date(2008, 12, 20), 'regular', padre_usuario='padre1')

        self.stdout.write("\n✅ Datos demo creados correctamente.")
