from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='advising-portal-home'),
    path('select-section/<section_id>/', views.add_course, name='advising-portal-select-course'),
    path('drop-section/<section_id>/', views.drop_course, name='advising-portal-drop-course'),
    path('selected_courses/', views.view_selected_courses, name='advising-portal-selected-courses'),
    path('grade_report/', views.view_grade_report, name='advising-portal-selected-courses'),
]
