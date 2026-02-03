"""Plan forms — ModelForms for sections, targets, metrics."""
from django import forms

from apps.programs.models import Program

from .models import MetricDefinition, PlanSection, PlanTarget


class PlanSectionForm(forms.ModelForm):
    """Form for creating/editing a plan section."""

    program = forms.ModelChoiceField(
        queryset=Program.objects.filter(status="active"),
        required=False,
        empty_label="No programme",
    )

    class Meta:
        model = PlanSection
        fields = ["name", "program", "sort_order"]
        widgets = {
            "sort_order": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Section name"
        self.fields["sort_order"].initial = 0


class PlanSectionStatusForm(forms.ModelForm):
    """Form for changing section status with a reason."""

    class Meta:
        model = PlanSection
        fields = ["status", "status_reason"]
        widgets = {
            "status": forms.Select(choices=PlanSection.STATUS_CHOICES),
            "status_reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for status change (optional)"}),
        }


class PlanTargetForm(forms.ModelForm):
    """Form for creating/editing a plan target."""

    class Meta:
        model = PlanTarget
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Target name"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe this target"}),
        }


class PlanTargetStatusForm(forms.ModelForm):
    """Form for changing target status with a reason."""

    class Meta:
        model = PlanTarget
        fields = ["status", "status_reason"]
        widgets = {
            "status": forms.Select(choices=PlanTarget.STATUS_CHOICES),
            "status_reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for status change (optional)"}),
        }


class MetricAssignmentForm(forms.Form):
    """Form for assigning metrics to a target (checkboxes)."""

    metrics = forms.ModelMultipleChoiceField(
        queryset=MetricDefinition.objects.filter(is_enabled=True, status="active"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assigned metrics",
    )


class MetricDefinitionForm(forms.ModelForm):
    """Form for creating/editing a metric definition."""

    class Meta:
        model = MetricDefinition
        fields = ["name", "definition", "category", "min_value", "max_value", "unit"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Metric name"}),
            "definition": forms.Textarea(attrs={"rows": 4, "placeholder": "What this metric measures and how to score it"}),
            "min_value": forms.NumberInput(attrs={"step": "any"}),
            "max_value": forms.NumberInput(attrs={"step": "any"}),
            "unit": forms.TextInput(attrs={"placeholder": "e.g., score, days, %"}),
        }


class MetricImportForm(forms.Form):
    """Form for uploading a CSV file of metric definitions."""

    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV with columns: name, definition, category, min_value, max_value, unit",
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data["csv_file"]
        if not csv_file.name.endswith(".csv"):
            raise forms.ValidationError("File must be a .csv file.")
        if csv_file.size > 1024 * 1024:  # 1MB limit
            raise forms.ValidationError("File too large. Maximum size is 1MB.")
        return csv_file
