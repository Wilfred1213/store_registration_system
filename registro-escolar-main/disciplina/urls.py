from django.urls import path

from .views import exportar_faltas_disciplinarias_de_periodo_escolar_activo

app_name = "disciplina"

urlpatterns = [
    path(
        "exportar-faltas-disciplinarias-de-periodo-escolar-activo",
        exportar_faltas_disciplinarias_de_periodo_escolar_activo,
        name="exportar_faltas_disciplinarias_de_periodo_escolar_activo",
    )
]
