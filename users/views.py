from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from advising_portal.forms import StudentRegisterForm
from .forms import UserRegisterForm, UserUpdateFrom, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        s_form = StudentRegisterForm(request.POST)

        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('login')

    else:
        u_form = UserRegisterForm()
        s_form = StudentRegisterForm()

    context = {
        'u_form': u_form,
        's_form': s_form
    }

    # return render(request, 'users/register.html', {'form': u_form})
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
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
