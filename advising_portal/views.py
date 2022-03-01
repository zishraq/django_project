from django.shortcuts import render
from django.http import HttpResponse
from .models import Courses


def home(request):
    context = {
        'posts': Courses.objects.all()
    }
    return render(request, 'advising_portal/home.html', context)
