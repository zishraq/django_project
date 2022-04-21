from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='advising-portal-home'),
    path('advising/', views.advising_portal_list_view, name='advising-portal-portal'),
    path('select-section/<section_id>/', views.add_course_view, name='advising-portal-select-course'),
    path('drop-section/<section_id>/', views.drop_course_view, name='advising-portal-drop-course'),

    path('request-section/', views.request_section_list_view, name='advising-portal-request-section-list-view'),
    # path('make-section-request/<section_id>/', views.request_section, name='advising-portal-make-section-request'),
    path('revoke-section-request/<section_id>/', views.revoke_section_request_view, name='advising-portal-revoke-section-request'),

    # path('selected-courses/', views.view_selected_courses, name='advising-portal-selected-courses'),
    path('grade-report/', views.view_grade_report, name='advising-portal-grade-report'),
]
