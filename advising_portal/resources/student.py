from django.contrib.auth.models import User

from advising_portal.models import Faculty, Student

students = [
    {
        'student_id': '2019-2-60-022',
        'name': 'Zuhair Ishraq Zareef',
        'advisor_id': Faculty.objects.get(faculty_id='AKD').pk,
    },
    {
        'student_id': '2019-2-60-015',
        'name': 'Nusrat Maisha',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
    },
    {
        'student_id': '2019-2-60-025',
        'name': 'Md. Tanvir Mobasshir',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk
    },
    {
        'student_id': '2018-2-60-127',
        'name': 'A. K. M. Sadat',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk
    },
    {
        'student_id': '2020-1-60-226',
        'name': 'Sofia Noor Rafa',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
    },
    {
        'student_id': '2020-1-65-001',
        'name': 'Komol Kunty Rajib',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
        'username_id': User.objects.get(username='2020-1-65-001').pk
    },
    {
        'student_id': 'admin',
        'name': 'admin',
        'advisor_id': Faculty.objects.get(faculty_id='admin').pk,
        'username_id': User.objects.get(username='admin').pk
    }
]

for i in students:
    r = Student(**i)
    r.save()
