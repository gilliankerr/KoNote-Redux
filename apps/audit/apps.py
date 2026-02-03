from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
    label = "audit"
    verbose_name = "Audit Log"

    def ready(self):
        # Import checks module to register Django system checks
        from . import checks  # noqa: F401
