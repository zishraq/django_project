from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='student-panel-home'),
    path('advising/<section_filter>/', views.advising_portal_list_view, name='student-panel-portal'),
    path('select-section/<section_id>/', views.add_course_view, name='student-panel-select-course'),
    path('drop-section/<section_id>/', views.drop_course_view, name='student-panel-drop-course'),

    path('request-section/', views.request_section_list_view, name='student-panel-request-section-list-view'),
    # path('make-section-request/<section_id>/', views.request_section, name='advising-portal-make-section-request'),
    path('revoke-section-request/<section_id>/', views.revoke_section_request_view, name='student-panel-revoke-section-request'),

    # path('selected-courses/', views.view_selected_courses, name='advising-portal-selected-courses'),
    path('advised-courses/', views.view_advised_courses, name='student-panel-advised-courses'),
    path('grade-report/', views.grade_report_view, name='student-panel-grade-report'),

    path('all-courses/', views.courses_list_view, name='student-panel-courses')
]
