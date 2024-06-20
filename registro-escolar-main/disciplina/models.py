# # Importing models from Django and other models from the project
# from django.db import models
# from escuela.models import PeriodoEscolar  # School period model
# from personas.models import Estudiante  # Student model

# # Define a model for a Failure (Falta in Spanish)
# class Falta(models.Model):
#     # Define choices for failure category
#     CATEGORIA_CHOICES = (("L", "Mild"), ("G", "Severe"), ("M", "Very Severe"))
#     # Fields for the model
#     codigo = models.PositiveSmallIntegerField(verbose_name="Code")
#     categoria = models.CharField(
#         verbose_name="Category", max_length=1, choices=CATEGORIA_CHOICES, default="L"
#     )
#     descripcion = models.TextField(verbose_name="Description")

#     def __str__(self):
#         return f"{self.codigo} {self.get_categoria_display()} {self.descripcion[:50]}..."

# # Define a model for a Student's Disciplinary Failure (Falta Disciplinaria Estudiantil in Spanish)
# class FaltaDisciplinariaEstudiantil(models.Model):
#     # Foreign key to the Student model
#     estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
#     # Foreign key to the Failure model
#     falta = models.ForeignKey(Falta, on_delete=models.CASCADE)
#     # Date field for when the failure occurred
#     fecha = models.DateField(help_text="Date the failure occurred")
#     # Text field for a description
#     descripcion = models.TextField(verbose_name="Description")
#     # Foreign key to the School Period model
#     periodo_escolar = models.ForeignKey(to=PeriodoEscolar, on_delete=models.PROTECT)

#     class Meta:
#         verbose_name = "Student Disciplinary Failure"
#         verbose_name_plural = "Student Disciplinary Failures"

#     def __str__(self):
#         return f"{self.falta.descripcion[:50]}..., {self.fecha}"
    
#     def clean(self) -> None:
#         # Set the school period to the active one
#         self.periodo_escolar = PeriodoEscolar.objects.get(periodo_activo=True)




from django.db import models
from escuela.models import PeriodoEscolar

from personas.models import Estudiante


class Falta(models.Model):
    CATEGORIA_CHOICES = (("L", "Leve"), ("G", "Grave"), ("M", "Muy Grave"))
    codigo = models.PositiveSmallIntegerField(verbose_name="código")
    categoria = models.CharField(
        verbose_name="categoría", max_length=1, choices=CATEGORIA_CHOICES, default="L"
    )
    descripcion = models.TextField(verbose_name="descripción")

    def __str__(self):
        return f"{self.codigo} {self.get_categoria_display()} {self.descripcion[:50]}..."


class FaltaDisciplinariaEstudiantil(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    falta = models.ForeignKey(Falta, on_delete=models.CASCADE)
    fecha = models.DateField(help_text="Fecha en que se cometió la falta")
    descripcion = models.TextField(verbose_name="Descripción")
    periodo_escolar = models.ForeignKey(to=PeriodoEscolar, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "falta disciplinaria de estudiante"
        verbose_name_plural = "faltas disciplinarias de estudiantes"

    def __str__(self):
        return f"{self.falta.descripcion[:50]}..., {self.fecha}"
    
    def clean(self) -> None:
        self.periodo_escolar = PeriodoEscolar.objects.get(periodo_activo=True)
