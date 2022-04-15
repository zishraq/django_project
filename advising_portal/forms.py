from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from advising_portal.models import Student, Faculty, SectionsRequested
# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class SectionRequestForm(forms.ModelForm):
    class Meta:
        model = SectionsRequested
        fields = ['reason']
