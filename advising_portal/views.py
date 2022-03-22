from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
# from .models import Course, TimeSlot
from advising_portal.models import Course, Section
import datetime


def home(request):
    context = {
        'sections': Section.objects.all()
    }
    return render(request, 'advising_portal/home.html', context)
