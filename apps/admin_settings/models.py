"""Instance customisation: terminology, features, and settings."""
from django.db import models


# Default terminology — keys must match template usage
DEFAULT_TERMS = {
    "client": "Client",
    "client_plural": "Clients",
    "file": "File",
    "plan": "Plan",
    "section": "Section",
    "target": "Target",
    "target_plural": "Targets",
    "metric": "Metric",
    "metric_plural": "Metrics",
    "progress_note": "Progress Note",
    "progress_note_plural": "Progress Notes",
    "quick_note": "Quick Note",
    "event": "Event",
    "program": "Program",
    "program_plural": "Programs",
    "alert": "Alert",
}


class TerminologyOverride(models.Model):
    """Stores custom terminology for this instance."""

    term_key = models.CharField(max_length=100, unique=True)
    display_value = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "admin_settings"
        db_table = "terminology_overrides"

    def __str__(self):
        return f"{self.term_key} → {self.display_value}"

    @classmethod
    def get_all_terms(cls):
        """Return merged dict of defaults + overrides."""
        terms = dict(DEFAULT_TERMS)
        overrides = dict(cls.objects.values_list("term_key", "display_value"))
        terms.update(overrides)
        return terms


class FeatureToggle(models.Model):
    """Feature flags for this instance."""

    feature_key = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=False)
    config_json = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "admin_settings"
        db_table = "feature_toggles"

    def __str__(self):
        state = "ON" if self.is_enabled else "OFF"
        return f"{self.feature_key}: {state}"

    @classmethod
    def get_all_flags(cls):
        """Return dict of feature_key → is_enabled."""
        return dict(cls.objects.values_list("feature_key", "is_enabled"))


class InstanceSetting(models.Model):
    """Key-value settings for branding, formats, timeouts, etc."""

    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "admin_settings"
        db_table = "instance_settings"

    def __str__(self):
        return f"{self.setting_key}: {self.setting_value[:50]}"

    @classmethod
    def get_all(cls):
        """Return dict of all settings."""
        return dict(cls.objects.values_list("setting_key", "setting_value"))

    @classmethod
    def get(cls, key, default=""):
        """Get a single setting value."""
        try:
            return cls.objects.get(setting_key=key).setting_value
        except cls.DoesNotExist:
            return default
