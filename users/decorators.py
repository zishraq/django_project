from django.http import HttpResponse
from django.shortcuts import redirect, render


def allowed_users(allowed_roles: list):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # return HttpResponse('You are not authorized to view this page')
                return render(request, 'advising_portal/401.html')

        return wrapper_func

    return decorator
