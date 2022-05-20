from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from advising_portal.models import Student
from advising_portal.utilities import get_referer_url
from users.forms import StudentProfileUpdateForm, ProfileActivationForm, ProfilePasswordForm, UserUpdateFrom, \
    FacultyProfileUpdateForm
from users.models import OTPmodel
from users.send_otp import send_otp, store_otp


def login_view(request):
    if not request.user.is_anonymous:
        return redirect('student-panel-home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if request.user.groups.all()[0].name == 'student':
                    messages.success(request, 'Welcome to East West University Student Portal!')

                return redirect('student-panel-home')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    form = AuthenticationForm()
    return render(
        request=request,
        template_name="users/login.html",
        context={
            'login_form': form
        }
    )


def activate_student_profile_view(request):
    if not request.user.is_anonymous:
        return redirect('student-panel-home')

    current_time = timezone.now()

    if request.method == 'POST':
        form = ProfileActivationForm(request.POST)

        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')

            existence_check = Student.objects.filter(
                student_id=student_id
            ).exists()

            if not existence_check:
                messages.error(request, 'No such Student')
                return redirect('activate')

            student_data = Student.objects.get(
                student_id=student_id
            )

            if student_data.username:
                messages.error(request, 'Profile already activated')
                return redirect('activate')

            otp_outputs = store_otp(student_id, current_time)

            receiver_mail = otp_outputs['receiver_mail']
            otp = otp_outputs['otp']
            otp_id = otp_outputs['otp_id']

            sent_otp = send_otp(
                receiver_mail=receiver_mail,
                otp=otp,
                reset_password=False
            )

            if not sent_otp['success']:
                messages.error(request, sent_otp['error'])
                return redirect('activate')

            messages.success(request, f'OTP sent successfully!')
            return redirect('set_password', otp_id=otp_id)

    else:
        form = ProfileActivationForm()

    context = {
        'form': form
    }

    # return render(request, 'users/activate.html', context)
    return render(request, 'users/register.html', context)


def forgot_password_view(request):
    if not request.user.is_anonymous:
        return redirect('student-panel-home')

    current_time = timezone.now()

    if request.method == 'POST':
        form = ProfileActivationForm(request.POST)

        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')

            student_existence_check = Student.objects.filter(
                student_id=student_id
            ).exists()

            if not student_existence_check:
                messages.error(request, 'No such Student')
                return redirect('forgot_password')

            user_existence_check = User.objects.filter(
                username=student_id
            ).exists()

            if not user_existence_check:
                messages.error(request, "Account hasn't been activated yet")
                return redirect('activate')

            otp_outputs = store_otp(student_id, current_time)

            receiver_mail = otp_outputs['receiver_mail']
            otp = otp_outputs['otp']
            otp_id = otp_outputs['otp_id']

            sent_otp = send_otp(
                receiver_mail=receiver_mail,
                otp=otp,
                reset_password=True
            )

            if not sent_otp['success']:
                messages.error(request, sent_otp['error'])
                return redirect('forgot_password')

            messages.success(request, f'OTP sent successfully!')
            return redirect('reset_password', otp_id=otp_id)

    else:
        form = ProfileActivationForm(None)

    context = {
        'form': form
    }

    return render(request, 'users/forgot_password2.html', context)


def set_password_view(request, otp_id):
    if not request.user.is_anonymous:
        return redirect('student-panel-home')

    current_time = timezone.now()

    if request.method == 'POST':
        form = ProfilePasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            received_otp = form.cleaned_data.get('otp')

            otp_data = OTPmodel.objects.get(
                otp_id=otp_id
            )

            if otp_data.otp != received_otp:
                messages.error(request, 'OTP mismatched')
                return redirect('set_password', otp_id=otp_id)

            if current_time > otp_data.expired_at:
                messages.error(request, 'OTP expired! Activate Again')
                return redirect('set_password', otp_id=otp_id)

            student_id = otp_data.student_id

            new_user = User.objects.create_user(
                username=student_id,
                email=f'{student_id}@std.ewubd.edu',
                password=password,
            )

            new_user.save()

            student_data = Student.objects.get(
                student_id=student_id
            )

            if not student_data.username:
                student_data.username = new_user
                student_data.save()

                group = Group.objects.get(name='student')
                group.user_set.add(new_user)

            else:
                messages.success(request, f'Account already activated for ID {student_id}!')
                return redirect('set_password', otp_id=otp_id)

            otp_data.is_successful = True
            otp_data.save()

            messages.success(request, f'Account created successfully for {student_id}!')
            return redirect('login')

    else:
        form = ProfilePasswordForm()

    context = {
        'form': form
    }

    # return render(request, 'users/activate.html', context)
    return render(request, 'users/set_password.html', context)


def reset_password_view(request, otp_id):
    if not request.user.is_anonymous:
        return redirect('student-panel-home')

    current_time = timezone.now()

    if request.method == 'POST':
        form = ProfilePasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            received_otp = form.cleaned_data.get('otp')

            otp_data = OTPmodel.objects.get(
                otp_id=otp_id
            )

            if otp_data.otp != received_otp:
                messages.error(request, 'OTP mismatched')
                return redirect('reset_password', otp_id=otp_id)

            if current_time > otp_data.expired_at:
                messages.error(request, 'OTP expired! Resend OTP')
                return redirect('reset_password', otp_id=otp_id)

            student_id = otp_data.student_id

            update_user = User.objects.get(
                username=student_id
            )
            update_user.set_password(password)
            update_user.save()

            otp_data.is_successful = True
            otp_data.save()

            messages.success(request, f'Password has been reset successfully for {student_id}!')
            return redirect('login')

    else:
        form = ProfilePasswordForm(None)

    context = {
        'form': form
    }

    return render(request, 'users/reset_password.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        if request.user.groups.all()[0].name == 'chairman' or request.user.groups.all()[0].name == 'faculty':
            p_form = FacultyProfileUpdateForm(request.POST, request.FILES, instance=request.user.faculty)
        else:
            p_form = StudentProfileUpdateForm(request.POST, request.FILES, instance=request.user.student)

        # if u_form.is_valid() and p_form.is_valid():
        if p_form.is_valid():
            # u_form.save()
            p_form.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        # u_form = UserUpdateFrom(instance=request.user)
        if request.user.groups.all()[0].name == 'chairman' or request.user.groups.all()[0].name == 'faculty':
            p_form = FacultyProfileUpdateForm(instance=request.user.faculty)
        else:
            p_form = StudentProfileUpdateForm(instance=request.user.student)

    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
