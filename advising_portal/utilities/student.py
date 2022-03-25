from django.contrib.auth.models import User

from advising_portal.models import Faculty, Student


students = [
    {
        'student_id': '2019-2-60-022',
        'name': 'Alex Steiner',
        'advisor_id': Faculty.objects.get(faculty_id='AKD').pk,
        'username_id': User.objects.get(username='alex').pk
    },
    {
        'student_id': '2019-2-60-021',
        'name': 'Zuhair Ishraq Zareef',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
        'username_id': User.objects.get(username='ishraq').pk
    },
    {
        'student_id': 'admin',
        'name': 'Zuhair Ishraq Zareef',
        'advisor_id': Faculty.objects.get(faculty_id='admin').pk,
        'username_id': User.objects.get(username='admin').pk
    }
]

for i in students:
    r = Student(**i)
    r.save()
