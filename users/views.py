import datetime
import uuid

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from advising_portal.models import Student
from .forms import ProfileUpdateForm, ProfileActivationForm, ProfilePasswordForm, UserUpdateFrom
from .models import OTPmodel
from .send_otp import generate_otp, send_otp, send_otp_forgot_password


def activate_profile_view(request):
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

            otp = generate_otp()
            receiver_mail = f'{student_id}@std.ewubd.edu'

            otp_id = str(uuid.uuid4())
            otp_data = {
                'otp_id': otp_id,
                'otp': otp,
                'student_id': student_id,
                'created_at': current_time,
                'expired_at': current_time + datetime.timedelta(minutes=2),
            }

            otp_store = OTPmodel(**otp_data)
            otp_store.save()

            sent_otp = send_otp(
                receiver_mail=receiver_mail,
                otp=otp
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

    return render(request, 'users/activate.html', context)


def forgot_password_view(request):
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


            otp = generate_otp()
            receiver_mail = f'{student_id}@std.ewubd.edu'

            otp_id = str(uuid.uuid4())
            otp_data = {
                'otp_id': otp_id,
                'otp': otp,
                'student_id': student_id,
                'created_at': current_time,
                'expired_at': current_time + datetime.timedelta(minutes=2),
            }

            otp_store = OTPmodel(**otp_data)
            otp_store.save()

            sent_otp = send_otp_forgot_password(
                receiver_mail=receiver_mail,
                otp=otp
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

    return render(request, 'users/forgot_password.html', context)


def set_password_view(request, otp_id):
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

    return render(request, 'users/activate.html', context)


def reset_password_view(request, otp_id):
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
                messages.error(request, 'OTP expired! Activate Again')
                return redirect('reset_password', otp_id=otp_id)

            student_id = otp_data.student_id

            update_user = User.objects.filter(
                username=student_id
            ).update(
                password=password
            )

            update_user.save()

            student_data = Student.objects.get(
                student_id=student_id
            )

            otp_data.is_successful = True
            otp_data.save()

            messages.success(request, f'Password has been reset successfully for {student_id}!')
            return redirect('login')

    else:
        form = ProfilePasswordForm()

    context = {
        'form': form
    }

    return render(request, 'users/forgot_password.html', context)



@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateFrom(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.student)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateFrom(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.student)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
