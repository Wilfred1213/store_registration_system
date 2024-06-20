import datetime
from tempfile import NamedTemporaryFile
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from openpyxl import Workbook

from escuela.models import PeriodoEscolar
from .models import FaltaDisciplinariaEstudiantil


def exportar_faltas_disciplinarias_de_periodo_escolar_activo(request):
    """
    vista que exporta a un archivo de Excel las faltas disciplinarias
    de todos los estudiantes durante el período activo, ordenados por
    seccion y luego por estudiante, si un estudiante tiene varias faltas
    deben salir consecutivamente por fecha.
    """
    if request.user.es_administrador():
        periodo_escolar_activo = PeriodoEscolar.objects.get(periodo_activo=True)
        faltas_de_periodo_escolar_activo = (
            FaltaDisciplinariaEstudiantil.objects.filter(
                periodo_escolar=periodo_escolar_activo
            )
            .select_related(
                "estudiante",
                "estudiante__seccion__nivel_educativo",
                "falta"
            )
            .order_by(
                "estudiante__seccion", "estudiante__apellidos", "estudiante__nombre"
            )
        )
        wb = Workbook()
        ws = wb.active
        ws.title = "Faltas de estudiantes"
        ws.column_dimensions["A"].width = 40
        ws.column_dimensions["B"].width = 25
        ws.column_dimensions["C"].width = 11
        ws.column_dimensions["D"].width = 50
        ws.column_dimensions["E"].width = 50
        ws.column_dimensions["F"].width = 12
        ws.append(
            [
                "Estudiante",
                "Sección",
                "Tipo de Falta",
                "Falta Cometida",
                "Descripción de la falta",
                "Fecha",
            ]
        )
        for falta in faltas_de_periodo_escolar_activo:
            ws.append(
                [
                    str(falta.estudiante),
                    str(falta.estudiante.seccion),
                    str(falta.falta.get_categoria_display()),
                    str(falta.falta.descripcion),
                    falta.descripcion,
                    falta.fecha,
                ]
            )
        with NamedTemporaryFile() as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()

            response = HttpResponse(
                content=stream,
                content_type="application/ms-excel",
            )
            response[
                "Content-Disposition"
            ] = f'attachment; filename=Faltas disciplinarias de estudiantes-{datetime.date.today().strftime("%Y_%m_%d")}.xlsx'
        return response
    else:
        raise PermissionDenied
