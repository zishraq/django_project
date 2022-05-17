from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='student-panel-home'),
    path('insert-test-data/', views.insert_test_data, name='student-panel-insert-test-data'),

    path('advising/<section_filter>/', views.advising_portal_list_view, name='student-panel-portal'),
    path('select-section/<section_id>/', views.add_course_view, name='student-panel-select-course'),
    path('drop-section/<section_id>/', views.drop_course_view, name='student-panel-drop-course'),

    path('request-section/', views.request_section_list_view, name='student-panel-request-section-list-view'),
    # path('make-section-request/<section_id>/', views.request_section, name='advising-portal-make-section-request'),
    path('revoke-section-request/<section_id>/', views.revoke_section_request_view, name='student-panel-revoke-section-request'),
    path('requested-section-conflict-check/<section_id>/', views.get_conflicting_sections_with_requested_section, name='requested-section-conflict-check'),

    path('advised-courses/', views.advised_course_list_view, name='student-panel-advised-courses'),
    path('grade-report/', views.grade_report_view, name='student-panel-grade-report'),

    path('course-list/', views.course_list_view, name='faculty-panel-course-list'),
    path('course-detail/<course_id>', views.course_detail_view, name='faculty-panel-course-detail'),
    path('course-create/', views.course_create_view, name='faculty-panel-course-create'),
    path('course-delete/<course_id>', views.course_delete_view, name='faculty-panel-course-delete'),
    path('course-log/<course_id>', views.course_log_view, name='student-panel-course-log'),

    path('section-detail/<section_id>', views.section_detail_view, name='faculty-panel-section-detail'),
    path('section-create/<course_code>', views.section_create_view, name='faculty-panel-section-create'),
    path('section-delete/<section_id>', views.section_delete_view, name='faculty-panel-section-delete'),

    path('semester-list/', views.semester_list_view, name='faculty-panel-semester-list'),
    path('semester-detail/<semester_id>', views.semester_detail_view, name='faculty-panel-semester-detail'),
    path('semester-create/', views.semester_create, name='faculty-panel-semester-create'),
    path('semester-delete/<semester_id>', views.semester_delete_view, name='student-panel-semester-delete'),
    path('semester-log/<semester_id>', views.semester_log_view, name='student-panel-semester-log'),

    path('section-request-list/', views.section_request_list_view, name='faculty-panel-section-request-list'),
    path('section-request-detail/<request_id>', views.section_request_detail_view, name='faculty-panel-section-request-detail'),

    path('student-list/', views.student_list_view, name='faculty-panel-student-list'),
    path('student-detail/<student_id>', views.student_detail_view, name='faculty-panel-student-detail'),
    # path('student-create/', views.semester_create, name='student-panel-semester-create'),

    path('assigned-sections/', views.assigned_sections, name='student-panel-assigned-sections')
]
