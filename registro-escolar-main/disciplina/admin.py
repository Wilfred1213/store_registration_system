from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from escuela.models import PeriodoEscolar
from escuela.admin import escuela_admin

from .models import Falta, FaltaDisciplinariaEstudiantil


class FaltaAdmin(admin.ModelAdmin):
    list_display = ["codigo", "categoria", "descripcion"]


class FaltaDisciplinariaEstudiantilAdmin(admin.ModelAdmin):
    list_display = ["estudiante", "fecha", "descripcion"]
    autocomplete_fields = ["estudiante"]
    search_fields = ["estudiante__nombre", "estudiante__apellidos"]

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.periodo_escolar.periodo_activo
        return super().has_change_permission(request, obj)


class FaltaDisciplinariaEstudiantilInline(admin.TabularInline):
    model = FaltaDisciplinariaEstudiantil
    fields = ["ver", "falta", "descripcion", "fecha"]
    readonly_fields = ["ver", "falta", "descripcion", "fecha"]
    extra = 0
    show_change_link = True
    verbose_name_plural = "Faltas disciplinarias cometidas por el estudiante"
    template = "admin/faltas_de_estudiante_inline.html"

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def get_queryset(self, request):
        periodo_escolar_activo = PeriodoEscolar.objects.get(periodo_activo=True)
        return (
            super()
            .get_queryset(request)
            .filter(fecha__gt=periodo_escolar_activo.fecha_de_inicio)
        )
    
    def ver(self, instance):
        """
        Agregamos un campo que enlaza a el Admin Change View
        de el objeto.
        """
        url = reverse(
            "escuela_admin:%s_%s_change"
            % (instance._meta.app_label, instance._meta.model_name),
            args=(instance.pk,),
        )
        return format_html('<a class="viewlink" href="{}">Ver</a>', url)


admin.site.register(Falta, FaltaAdmin)
admin.site.register(FaltaDisciplinariaEstudiantil, FaltaDisciplinariaEstudiantilAdmin)

escuela_admin.register(Falta, FaltaAdmin)
escuela_admin.register(
    FaltaDisciplinariaEstudiantil, FaltaDisciplinariaEstudiantilAdmin
)
