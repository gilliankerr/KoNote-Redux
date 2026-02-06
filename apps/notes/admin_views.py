"""Admin views for progress note templates."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import NoteTemplateForm, NoteTemplateSectionForm
from .models import ProgressNoteTemplate, ProgressNoteTemplateSection


SectionFormSet = inlineformset_factory(
    ProgressNoteTemplate,
    ProgressNoteTemplateSection,
    form=NoteTemplateSectionForm,
    extra=1,
    can_delete=True,
)


def _admin_required(view_func):
    """Decorator: require admin role."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseForbidden("Access denied.")
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


@_admin_required
def template_list(request):
    templates = ProgressNoteTemplate.objects.all()
    return render(request, "notes/admin/template_list.html", {"templates": templates})


@_admin_required
def template_create(request):
    if request.method == "POST":
        form = NoteTemplateForm(request.POST)
        formset = SectionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            template = form.save()
            formset.instance = template
            formset.save()
            messages.success(request, _("Note template created."))
            return redirect("note_templates:template_list")
    else:
        form = NoteTemplateForm()
        formset = SectionFormSet()
    return render(request, "notes/admin/template_form.html", {
        "form": form,
        "formset": formset,
        "editing": False,
    })


@_admin_required
def template_edit(request, pk):
    template = get_object_or_404(ProgressNoteTemplate, pk=pk)
    if request.method == "POST":
        form = NoteTemplateForm(request.POST, instance=template)
        formset = SectionFormSet(request.POST, instance=template)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("Note template updated."))
            return redirect("note_templates:template_list")
    else:
        form = NoteTemplateForm(instance=template)
        formset = SectionFormSet(instance=template)
    return render(request, "notes/admin/template_form.html", {
        "form": form,
        "formset": formset,
        "editing": True,
        "template": template,
    })
