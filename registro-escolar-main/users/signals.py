from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# from .models import User
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def agregar_usuario_a_grupo(sender, instance, created, **kwargs):
    """
    Django Signal que agrega un usuario a un grupo.
    Un usuario se mantiene en uno y solo un grupo
    """
    if instance.es_administrador():
        try:
            administradores = Group.objects.get(name="Administradores")
            instance.groups.clear()
            instance.groups.add(administradores)
        except:
            pass
    elif instance.es_profesor():
        try:
            profesores = Group.objects.get(name="Profesores")
            instance.groups.clear()
            instance.groups.add(profesores)
        except:
            pass
    elif instance.es_digitador():
        try:
            digitadores = Group.objects.get(name="Digitadores")
            instance.groups.clear()
            instance.groups.add(digitadores)
        except:
            pass
