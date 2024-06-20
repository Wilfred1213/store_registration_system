import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError

from django.db import models
from django.urls import reverse

from escuela.models import Escuela, Seccion

from .helpers import normalizar_nombre_propio
from .validators import validate_date_is_past


class Relacion(models.TextChoices):
    PADRE = "P", "Padre"
    MADRE = "M", "Madre"
    TIO = "T", "Tío/Tía"
    ABUELO = "A", "Abuelo/Abuela"
    HERMANO = "H", "Hermano/Hermana"
    OTROS = "O", "Otros"


class Departamento(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.nombre} - {self.departamento}"


class Persona(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    SEXO_CHOICES = [("M", "Masculino"), ("F", "Femenino")]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default="F")
    fecha_de_nacimiento = models.DateField(validators=[validate_date_is_past])
    telefono_1 = models.CharField(
        verbose_name="Teléfono de contacto 1", max_length=20, blank=True, null=True
    )
    telefono_2 = models.CharField(
        verbose_name="Teléfono de contacto 2", max_length=20, blank=True, null=True
    )
    correo_electronico = models.EmailField(
        verbose_name="Correo electrónico personal", blank=True, null=True
    )

    @property
    def edad(self):
        hoy = datetime.date.today()
        diferencia_fechas = hoy - self.fecha_de_nacimiento
        edad = int(diferencia_fechas.days / 365.25)
        return edad

    def save(self, *args, **kwargs):
        self.nombre = normalizar_nombre_propio(self.nombre)
        self.apellidos = normalizar_nombre_propio(self.apellidos)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Responsable(Persona):
    class SituacionLaboral(models.TextChoices):
        EMPLEADO = "E", "Empleado"
        DESEMPLEADO = "D", "Desempleado"
        INFORMAL = "I", "Empleo Informal"
        AMA_DE_CASA = "A", "Ama de Casa"
        EMPRESARIO = "M", "Empresario"
        PROFESIONAL = "P", "Profesional autónomo"

    dui = models.CharField(verbose_name="DUI", max_length=25, unique=True)
    situacion_laboral = models.CharField(
        max_length=20,
        verbose_name="Situación Laboral",
        default="D",
        choices=SituacionLaboral.choices,
    )
    direccion_de_residencia = models.CharField(max_length=200, blank=True, null=True)
    observaciones = models.TextField(
        help_text="Ingrese información adicional relevante, como uso de otros documentos que no son DUI o alguna particularidad",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.apellidos}, {self.nombre}"


class Estudiante(Persona):
    nie = models.CharField(
        verbose_name="NIE", max_length=12, blank=True, null=True, unique=True
    )
    escuela_previa = models.ForeignKey(
        Escuela, on_delete=models.CASCADE, blank=True, null=True
    )
    seccion = models.ForeignKey(
        Seccion,
        verbose_name="Sección",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="estudiantes_en",
        limit_choices_to={"periodo_escolar__periodo_activo": True},
    )
    secciones = models.ManyToManyField(Seccion, related_name="estudiantes")
    posee_partida = models.BooleanField(
        verbose_name="Posee partida de nacimiento",
        help_text=(
            "Si el estudiante no posee partida de nacimiento se debe demostrar"
            " un trámite áctivo para obtenerla."
        ),
        default=True,
    )
    NACIONALIDAD_CHOICES = [
        ("S", "Salvadoreña"),
        ("H", "Hondureña"),
        ("G", "Guatemalteca"),
        ("N", "Nicaragüense"),
        ("C", "Costaricence"),
        ("P", "Panameña"),
        ("E", "Estadounidense"),
        ("O", "Otros"),
    ]
    nacionalidad = models.CharField(
        max_length=1, choices=NACIONALIDAD_CHOICES, default="S"
    )
    municipio_de_nacimiento = models.ForeignKey(
        Municipio, blank=True, null=True, on_delete=models.SET_NULL, default=1
    )
    direccion_de_residencia = models.CharField(
        verbose_name="Dirección de residencia", max_length=200, blank=True, null=True
    )
    municipio_de_residencia = models.ForeignKey(
        Municipio,
        related_name="reside_en",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        default=1,
    )
    ETNIA_CHOICES = [
        ("N", "Ninguna"),
        ("K", "Kakawira"),
        ("L", "Lenca"),
        ("N", "Nahuat-Pipil"),
    ]
    etnia = models.CharField(max_length=1, choices=ETNIA_CHOICES, default="N")
    es_autista = models.BooleanField(verbose_name="Transtorno del espectro autista")
    sordera = models.BooleanField()
    ceguera = models.BooleanField()
    baja_vision = models.BooleanField(verbose_name="Baja visión")
    down = models.BooleanField(verbose_name="Síndrome de Down", default=False)
    discapacidad_motora = models.BooleanField()
    discapacidad_intelectual = models.BooleanField()
    embarazo = models.BooleanField()
    otro = models.CharField(
        max_length=100,
        help_text="Describa cualquier condición adicional de salud.",
        blank=True,
        null=True,
    )
    usa_medicamentos = models.BooleanField(
        verbose_name="¿El estudiante toma algún medicamento prescrito permanentemente?",
        default=False,
    )
    medicamentos = models.CharField(
        max_length=200, verbose_name="Escriba el nombre de los medicamentos", blank=True
    )
    SANGRE_CHOICES = [
        ("A+", "A Rh positivo(A rh+)"),
        ("A-", "A Rh negativo(A rh-)"),
        ("B+", "B Rh positivo(B rh+)"),
        ("B-", "B Rh negativo(B rh-)"),
        ("O+", "O Rh positivo(O rh+)"),
        ("O-", "O Rh negativo(O rh-)"),
        ("AB+", "AB Rh positivo(AB rh+)"),
        ("AB-", "AB Rh negativo(AB rh-)"),
    ]
    tipo_de_sangre = models.CharField(max_length=3, choices=SANGRE_CHOICES, blank=True)

    ESTADO_CIVIL_CHOICES = [
        ("S", "Soltero"),
        ("C", "Casado"),
        ("D", "Divorciado"),
        ("U", "Unión libre"),
        ("O", "Otro"),
    ]
    estado_civil = models.CharField(
        max_length=1, choices=ESTADO_CIVIL_CHOICES, default="S"
    )
    ROOMMATE_CHOICES = [
        ("M", "Madre"),
        ("D", "Padre"),
        ("P", "Padre y madre"),
        ("F", "Otro familiar"),
        ("S", "Solo"),
        ("O", "Otros"),
    ]
    roommate = models.CharField(
        max_length=1,
        verbose_name="Personas con quienes vive el estudiante",
        choices=ROOMMATE_CHOICES,
        default="P",
    )
    trabaja = models.BooleanField(verbose_name="¿El Estudiante trabaja?")
    dependencia_economica = models.CharField(
        max_length=1, choices=ROOMMATE_CHOICES, default="P"
    )
    zona_de_residencia = models.CharField(
        max_length=1, choices=[("U", "Urbana"), ("R", "Rural")], default="U"
    )
    utiliza_vehiculo = models.BooleanField(verbose_name="Utiliza Vehículo")
    utiliza_transporte_publico = models.BooleanField(
        verbose_name="Utiliza transporte público"
    )
    camina_a_la_escuela = models.BooleanField()
    otro_medio_de_transporte = models.BooleanField()
    distancia = models.PositiveSmallIntegerField(
        verbose_name="Distancia de vivienda al centro escolar",
        help_text=(
            "Ingrese la distancia en KM de la vivienda"
            " del estudiante al centro educativo."
        ),
    )
    posee_refrigerador = models.BooleanField(default=True)
    posee_televisor = models.BooleanField(default=True)
    posee_celular_con_acceso_a_internet = models.BooleanField(default=True)
    posee_radio = models.BooleanField(
        verbose_name="Posee radio o equipo de sonido", default=True
    )
    posee_computadora = models.BooleanField()
    posee_tablet = models.BooleanField()
    posee_energia = models.BooleanField(
        verbose_name="Posee energía eléctrica", default=True
    )
    AGUA_CHOICES = [
        ("A", "Servicio de agua potable en casa"),
        ("P", "Pila, chorro público o cantarera"),
        ("Z", "Pozo"),
        ("I", "Pipa"),
        ("R", "Río, Laguna o nacimiento"),
        ("L", "Aguas lluvias"),
        ("O", "Otros"),
    ]
    fuente_de_agua = models.CharField(max_length=1, choices=AGUA_CHOICES, default="A")
    PISO_CHOICES = [
        ("L", "Ladrillo de cemento"),
        ("C", "Cerámica"),
        ("M", "Cemento"),
        ("T", "Tierra"),
        ("O", "Otro"),
    ]
    piso = models.CharField(
        max_length=1,
        help_text="Material principal del piso de la casa del estudiante",
        choices=PISO_CHOICES,
        default="L",
    )
    SANITARIO_CHOICES = [
        ("T", "Tasa conectada a alcantarillado"),
        ("F", "Fosa séptica"),
        ("O", "Otro"),
    ]
    tipo_de_sanitario = models.CharField(
        max_length=1, choices=SANITARIO_CHOICES, default="T"
    )
    internet_residencial = models.BooleanField()
    INTERNET_CHOICES = [
        ("T", "Tigo"),
        ("C", "Claro"),
        ("J", "Japi"),
        ("O", "Otro"),
    ]
    compania_internet = models.CharField(
        max_length=1,
        help_text="Si posee internet residencial indique la compañia.",
        choices=INTERNET_CHOICES,
        blank=True,
        null=True,
    )
    cantidad_cohabitantes = models.PositiveSmallIntegerField(
        help_text="Indique la cantidad de personas que vivien con el estudiante"
    )
    menores_en_casa = models.BooleanField(
        verbose_name="Viven menores de 18 años con el estudiante"
    )
    responsable = models.ForeignKey(
        Responsable,
        related_name="responsable_de",
        help_text="Persona autorizada a hacer trámites del estudiantes.",
        on_delete=models.PROTECT,
        null=True,
    )
    relacion_de_responsable = models.CharField(
        max_length=1,
        verbose_name="Relación familiar de responsable con estudiante.",
        choices=Relacion.choices,
        default=Relacion.MADRE,
    )
    estudiantes_en_la_misma_casa = models.ManyToManyField(
        "self",
        help_text=("Ingrese estudiantes que viven en la misma casa."),
        blank=True,
    )
    activo = models.BooleanField(
        help_text="Desmarcar si el estudiante retira documentos", default=True
    )
    retirado = models.BooleanField(
        help_text="Marcar si el estudiante se retira de la institución",
        default=False,
    )
    fecha_de_retiro = models.DateField(blank=True, null=True)
    motivo_de_retiro = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.apellidos}, {self.nombre} "

    @admin.display(boolean=True)
    def sobreedad(self):
        if self.seccion:
            return self.edad > self.seccion.nivel_educativo.edad_normal_de_ingreso + 1
        return False

    def get_absolute_url(self):
        return reverse("admin:personas_estudiante_change", args=(self.pk,))

    def clean(self):
        if self.seccion:
            try:
                if self.secciones.all():
                    seccion_mayor = self.secciones.order_by(
                        "-nivel_educativo__edad_normal_de_ingreso"
                    )[0]
                    if (
                        self.seccion.nivel_educativo.edad_normal_de_ingreso
                        > seccion_mayor.nivel_educativo.edad_normal_de_ingreso + 1
                    ):
                        raise ValidationError(
                            {
                                "seccion": "Solo puede matricular a un estudiante en mismo nivel o en el inmediato superior"
                            }
                        )
                    elif (
                        self.seccion.nivel_educativo.edad_normal_de_ingreso
                        < seccion_mayor.nivel_educativo.edad_normal_de_ingreso
                    ):
                        raise ValidationError(
                            {
                                "seccion": "Un estudiante no puede ser matriculado en un grado inferior a los ya cursados."
                            }
                        )
            except:
                pass
