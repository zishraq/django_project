"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_wsgi_application()


if __name__ == '__main__':
    import datetime
    import uuid
    from advising_portal.models import RoutineSlot, TimeSlot, Department, Course, Faculty, Section, Student, CoursesTaken, Semester
    from advising_portal.utilities.time_slot import time_slots
    from django.contrib.auth.models import User

    # str(uuid.uuid4())

    students = [
        {
            'student_id': '2019-2-60-022',
            'name': 'Alex Steiner',
            'advisor': Faculty.objects.get(faculty_id='AKD'),
            'user_id': User.objects.get(username='alex')
        }
    ]

    # for s in students:
    #     r = Student(**s)
    #     r.save()

    c = CoursesTaken.objects.get(
        student_id=Student.objects.get(user_id=User.objects.get(username='alex')),
        semester_id=Semester.objects.get(advising_status=True),
        section_id=Section.objects.get(section_id='CSE1031')
    )

    print(c)
