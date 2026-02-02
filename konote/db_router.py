"""Database router to direct audit models to the audit database."""


class AuditRouter:
    """Route audit app models to the 'audit' database."""

    audit_app = "audit"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.audit_app:
            return "audit"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.audit_app:
            return "audit"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within the same database
        if obj1._meta.app_label == self.audit_app or obj2._meta.app_label == self.audit_app:
            return obj1._meta.app_label == obj2._meta.app_label
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.audit_app:
            return db == "audit"
        if db == "audit":
            return False
        return None
