from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from advising_portal.models import Student, Faculty


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']


class ProfileActivationForm(forms.Form):
    student_id = forms.CharField(label='Student ID', max_length=100)


class ProfilePasswordForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=100)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
