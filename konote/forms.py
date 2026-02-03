"""Forms for AI-powered HTMX endpoints."""
from django import forms


class SuggestMetricsForm(forms.Form):
    """Form for the suggest-metrics AI endpoint."""

    target_description = forms.CharField(max_length=1000)


class ImproveOutcomeForm(forms.Form):
    """Form for the improve-outcome AI endpoint."""

    draft_text = forms.CharField(max_length=5000)


class GenerateNarrativeForm(forms.Form):
    """Form for the generate-narrative AI endpoint."""

    program_id = forms.IntegerField()
    date_from = forms.DateField()
    date_to = forms.DateField()


class SuggestNoteStructureForm(forms.Form):
    """Form for the suggest-note-structure AI endpoint."""

    target_id = forms.IntegerField()
