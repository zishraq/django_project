from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from advising_portal.models import Student, Faculty


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name']
