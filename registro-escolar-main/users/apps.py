from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "usuarios"
    verbose_name_plural = "usuarios"

    def ready(self):
        import users.signals