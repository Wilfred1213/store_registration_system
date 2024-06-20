
from debug_toolbar import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path
from django.views.generic.base import RedirectView

from escuela.admin import escuela_admin


urlpatterns = [
    path(
        "disciplina/",
        include("disciplina.urls"),
        name="disciplina"
    ),
    path(
        "restauracion_solicitada/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "restauracion_contrasena/",
        PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "confirmacion_restauracion/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "restauracion_completa",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("", RedirectView.as_view(url="administracion/")),
    path("admin/", admin.site.urls),
    path("administracion/", escuela_admin.urls),
    path("chaining/", include("smart_selects.urls")),
    path("__debug__/", include(urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
