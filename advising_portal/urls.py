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

    path('advised-courses/', views.advised_course_list_view, name='student-panel-advised-courses'),
    path('grade-report/', views.grade_report_view, name='student-panel-grade-report'),

    path('course-list/', views.course_list_view, name='student-panel-course-list'),
    path('course-detail/<course_id>', views.course_detail_view, name='student-panel-course-detail'),
    path('course-create/', views.course_create_view, name='student-panel-course-create'),

    path('section-create/<course_code>', views.section_create_view, name='student-panel-section-create'),
    path('section-detail/<section_id>', views.section_detail_view, name='student-panel-section-detail'),

    path('semester-list/', views.semester_list_view, name='student-panel-semester-list'),
    path('semester-detial/<semester_id>', views.semester_detail_view, name='student-panel-semester-detail'),
    path('semester-create/', views.semester_create, name='student-panel-semester-create'),

    # path('student-list/', views.semester_list_view, name='student-panel-semester-list'),
    # path('student-detial/<semester_id>', views.semester_detail_view, name='student-panel-semester-detail'),
    # path('student-create/', views.semester_create, name='student-panel-semester-create'),

    path('assigned-sections/', views.assigned_sections, name='student-panel-assigned-sections')
]
