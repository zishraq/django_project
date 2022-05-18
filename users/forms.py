from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from advising_portal.models import Student, Faculty


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean(self):
    #     cleaned_data = super(UserRegisterForm, self).clean()
    #     # additional cleaning here
    #     return cleaned_data


class UserUpdateFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_picture', 'name', 'advisor', 'gender', 'date_of_birth', 'address']

    def __init__(self, *args, **kwargs):
        super(StudentProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['advisor'].widget.attrs['readonly'] = True
        self.fields['gender'].widget.attrs['readonly'] = True


class FacultyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Faculty
        readonly_fields = ('name', 'initials')
        fields = ['profile_picture', 'date_of_birth', 'address']

    def __init__(self, *args, **kwargs):
        super(FacultyProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['initials'].required = False


class ProfileActivationForm(forms.Form):
    student_id = forms.CharField(label='Student ID', max_length=100)


class ProfilePasswordForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=100)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
