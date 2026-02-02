"""Forms for progress notes."""
from django import forms

from .models import ProgressNote


class QuickNoteForm(forms.ModelForm):
    """Simple form for quick notes — just a text area."""

    class Meta:
        model = ProgressNote
        fields = ["notes_text"]
        widgets = {
            "notes_text": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Write your note here...",
                "required": True,
            }),
        }

    def clean_notes_text(self):
        text = self.cleaned_data.get("notes_text", "").strip()
        if not text:
            raise forms.ValidationError("Note text is required.")
        return text
