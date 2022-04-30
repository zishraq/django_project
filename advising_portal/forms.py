from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from advising_portal.models import Student, Faculty, SectionsRequested, Course

# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class SectionRequestForm(forms.Form):
    reason = forms.CharField(label='reason', max_length=500, widget=forms.Textarea)
    section = forms.CharField(label='section', widget=forms.HiddenInput())


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_code', 'course_title', 'department', 'prerequisite_course', 'credit')
        # widgets = {
        #     'prerequisite_course': forms.Select
        # }

    def __init__(self, *args, **kwargs):
        super(CreateCourseForm, self).__init__(*args, **kwargs)
        self.fields['prerequisite_course'].required = False
