from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='advising-portal-home'),
    path('section/<section_id>/', views.select_course, name='advising-portal-select-course'),
]
