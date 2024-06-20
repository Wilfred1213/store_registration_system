from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from escuela.models import Seccion
from .models import Estudiante

@receiver(post_save, sender=Estudiante)
def agregar_seccion_a_estudiante(sender, instance, created, **kwargs):
    """
    Signal que agrega a un estudiantes la relación mucho a muchos la
    sección guardada si esta no está y además elimina cualquier otra sección
    que sea del mismo período 
    """
    if instance.seccion:
        try:
            if instance.seccion in instance.secciones.all():
                pass
            else:
                try:
                    seccion_a_eliminar = instance.secciones.get(periodo_escolar=instance.seccion.periodo_escolar)
                    instance.secciones.remove(seccion_a_eliminar)
                except:
                    pass
                finally:
                    instance.secciones.add(instance.seccion)
        except:
            instance.secciones.add(instance.seccion)