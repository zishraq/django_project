from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from django.forms import DateInput

from advising_portal.models import Student, Faculty, Course, Semester, Section


# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class SectionRequestForm(forms.Form):
    reason = forms.CharField(label='reason', max_length=500, widget=forms.Textarea)
    section = forms.CharField(label='section', widget=forms.HiddenInput())


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_code', 'course_title', 'department', 'prerequisite_course', 'credit')

    def __init__(self, *args, **kwargs):
        super(CreateCourseForm, self).__init__(*args, **kwargs)
        self.fields['prerequisite_course'].required = False


class CreateSemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('semester_name', 'semester_starts_at', 'semester_ends_at', 'advising_status', 'is_active', 'add_drop_status')
        widgets = {
            'semester_starts_at': DateInput(attrs={'type': 'date'}),
            'semester_ends_at': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(CreateSemesterForm, self).__init__(*args, **kwargs)
        self.fields['advising_status'].required = False
        self.fields['is_active'].required = False
        self.fields['add_drop_status'].required = False


class CreateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('section_no', 'section_capacity', 'instructor', 'routine')

    def __init__(self, *args, **kwargs):
        super(CreateSectionForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].required = False


class UpdateSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('section_capacity', 'instructor', 'routine')

    def __init__(self, *args, **kwargs):
        super(UpdateSectionForm, self).__init__(*args, **kwargs)
        self.fields['section_capacity'].required = False
        self.fields['instructor'].required = False
        self.fields['routine'].required = False
