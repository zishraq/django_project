from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from django.forms import DateInput, BooleanField

from advising_portal.models import Student, Faculty, Course, Semester, Section, SectionsRequested


# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from advising_portal.utilities import APPROVED, REJECTED


class SectionRequestForm(forms.Form):
    reason = forms.CharField(label='Reason', max_length=500, widget=forms.Textarea)
    section = forms.CharField(label='section', widget=forms.HiddenInput())


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('semester', 'course_code', 'course_title', 'department', 'prerequisite_course', 'credit')

    def __init__(self, *args, **kwargs):
        super(CreateCourseForm, self).__init__(*args, **kwargs)
        self.fields['prerequisite_course'].required = False


class CreateSemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('semester_name', 'semester_starts_at', 'semester_ends_at', 'advising_status', 'is_active', 'add_drop_status', 'seat_request_status')
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


# class UpdateSectionRequestForm(forms.ModelForm):
#     class Meta:
#         model = SectionsRequested
#         fields = ['is_approved_by_advisor', 'advisor_text', 'is_approved_by_chairman', 'chairman_text', 'is_approved_by_instructor', 'instructor_text']
#         labels = {
#             'is_approved_by_advisor': 'Approve',
#             'advisor_text': 'Text',
#             'is_approved_by_chairman': 'Approve',
#             'chairman_text': 'Text',
#             'is_approved_by_instructor': 'Approve',
#             'instructor_text': 'Text',
#         }
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request')
#         print(self.request.user)
#
#         super(UpdateSectionRequestForm, self).__init__(*args, **kwargs)
#
#         print(self.instance.student.name)
#
#         self.fields['advisor_text'].required = False


class UpdateSectionRequestForm(forms.Form):
    APPROVAL_STATUS = (
        (APPROVED, APPROVED),
        (REJECTED, REJECTED)
    )

    approval_status = forms.ChoiceField(label='Status', choices=APPROVAL_STATUS, widget=forms.RadioSelect)
    text = forms.CharField(label='Text', max_length=500, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UpdateSectionRequestForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = False


class StudentUpdateForm(forms.Form):
    class Meta:
        model = Student
        # readonly_fields = ('name', 'advisor', 'gender',)
        fields = ('name', 'advisor', 'gender')

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['advisor'].widget.attrs['readonly'] = True
        self.fields['gender'].widget.attrs['readonly'] = True

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.name
        else:
            return self.cleaned_data['name']

    def clean_advisor(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.advisor
        else:
            return self.cleaned_data['advisor']

    def clean_gender(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.gender
        else:
            return self.cleaned_data['gender']


class FacultyStudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'advisor', 'profile_picture', 'gender')

    def __init__(self, *args, **kwargs):
        super(FacultyStudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['advisor'].widget.attrs['readonly'] = True
        self.fields['gender'].widget.attrs['readonly'] = True

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.name
        else:
            return self.cleaned_data['name']

    def clean_advisor(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.advisor
        else:
            return self.cleaned_data['advisor']

    def clean_gender(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.gender
        else:
            return self.cleaned_data['gender']
