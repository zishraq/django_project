from django.contrib.auth.models import User

from advising_portal.models import Department, Course


courses = [
    {
        'course_id': 'CSE103',
        'course_code': 'CSE103',
        'course_title': 'Structured Programming',
        'department_id': Department.objects.get(pk='CSE'),
        'prerequisite_course_id': None,
        'credit': 3,
        'created_by': User.objects.get(username='admin')
    },
    {
        'course_id': 'CSE110',
        'course_code': 'CSE110',
        'course_title': 'Object Oriented Programming',
        'department_id': Department.objects.get(pk='CSE'),
        'prerequisite_course_id': None,
        'credit': 3,
        'created_by': User.objects.get(username='admin')
    }
]

for i in courses:
    r = Course(**i)
    r.save()