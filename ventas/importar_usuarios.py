import django
import os

# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ventas.settings")
django.setup()

from django.contrib.auth.models import User
from carro_compra.models import Usuario

# Migrar datos de `Usuario` a `User`
for usuario in Usuario.objects.all():
    user = User.objects.create_user(
        username=usuario.nom_usuario,
        password=usuario.contraseña,
        first_name=usuario.nombre,
        last_name=usuario.apellido
    )
    user.save()

# Opcional: Eliminar todos los objetos del modelo `Usuario` después de la migración
# Usuario.objects.all().delete()
