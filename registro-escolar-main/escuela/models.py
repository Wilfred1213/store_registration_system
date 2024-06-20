from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction


class Escuela(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(
        max_length=10, verbose_name="Código de infraestructura", blank=True, null=True
    )

    def __str__(self):
        return self.nombre


class PeriodoEscolar(models.Model):
    nombre = models.CharField(
        max_length=50,
        help_text='Ingrese el nombre del período escolar, por ejemplo: "Año escolar 2020',
    )
    fecha_de_inicio = models.DateField(
        help_text="Ingrese la fecha de inicio del período escolar"
    )
    fecha_de_cierre = models.DateField(
        help_text="Ingrese la fecha de cierre del período escolar"
    )
    periodo_activo = models.BooleanField(verbose_name="período activo", default=False)

    class Meta:
        verbose_name_plural = "períodos escolares"

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.fecha_de_cierre < self.fecha_de_inicio:
            raise ValidationError(
                {
                    "fecha_de_cierre": "La fecha de cierre debe ser posterior a la fecha de inicio"
                }
            )
        super(PeriodoEscolar, self).clean()

    def save(self, *args, **kwargs):
        if self.periodo_activo:
            with transaction.atomic():
                PeriodoEscolar.objects.filter(periodo_activo=True).update(
                    periodo_activo=False
                )
        super(PeriodoEscolar, self).save(*args, **kwargs)


class NivelEducativo(models.Model):
    nivel = models.CharField(max_length=50)
    edad_normal_de_ingreso = models.PositiveSmallIntegerField(
        help_text="Ingrese la edad normal en que los estudiantes deben estar en este nivel educativo",
        validators=[
            MinValueValidator(2),
            MaxValueValidator(18),
        ],
    )

    def total_estudiantes(self):
        total = 0
        for seccion in self.seccion_set.all():
            total += seccion.estudiante_set.count()
        return total

    def total_femenino(self):
        total = 0
        for seccion in self.seccion_set.all():
            total += seccion.estudiante_set.filter(sexo="F").count()
        return total

    def total_masculino(self):
        total = 0
        for seccion in self.seccion_set.all():
            total += seccion.estudiante_set.filter(sexo="M").count()
        return total

    def __str__(self):
        return self.nivel

    def edad_de_ingreso_al_nivel(self):
        return f"{self.edad_normal_de_ingreso} años."

    class Meta:
        verbose_name = "nivel educativo"
        verbose_name_plural = "niveles educativos"
        ordering = ["edad_normal_de_ingreso", "nivel"]


class Seccion(models.Model):
    periodo_escolar = models.ForeignKey(
        PeriodoEscolar, verbose_name="período escolar", on_delete=models.CASCADE
    )
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE)
    SECCION_CHOICES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("F", "F"),
        ("G", "G"),
        ("H", "H"),
        ("I", "I"),
        ("J", "J"),
        ("K", "K"),
        ("F", "F"),
        ("L", "L"),
        ("M", "M"),
        ("N", "N"),
    )
    seccion = models.CharField(
        verbose_name="sección", max_length=1, choices=SECCION_CHOICES, default="A"
    )

    def total_estudiantes(self):
        return self.estudiantes_en.count()

    def total_femenino(self):
        return self.estudiantes_en.filter(sexo="F").count()

    def total_masculino(self):
        return self.estudiantes_en.filter(sexo="M").count()

    def __str__(self):
        return f"{self.nivel_educativo} {self.seccion}"

    class Meta:
        verbose_name = "sección"
        verbose_name_plural = "secciones"
        ordering = [
            "nivel_educativo__edad_normal_de_ingreso",
            "nivel_educativo",
            "seccion",
        ]
