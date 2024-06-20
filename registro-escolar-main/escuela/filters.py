from typing import ClassVar
from django.contrib.admin import SimpleListFilter

from .models import PeriodoEscolar


class SeccionPorPeriodoFilter(SimpleListFilter):
    """
    Filtro que permite ver las secciones por período educativo
    """

    template = "django_admin_listfilter_dropdown/dropdown_filter.html"
    title = "Período Educativo"
    parameter_name = "periodo_escolar"

    def lookups(self, request, model_admin):
        return [
            (periodo.id, periodo.nombre) for periodo in PeriodoEscolar.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(periodo_escolar__id=self.value())
        else:
            return queryset.filter(periodo_escolar__periodo_activo=True)
