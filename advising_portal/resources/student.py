from django.contrib.auth.models import User

from advising_portal.models import Faculty, Student

students = [
    {
        'student_id': '2019-2-60-022',
        'name': 'Zuhair Ishraq Zareef',
        'gender': 'male',
        'advisor_id': Faculty.objects.get(faculty_id='AKD').pk,
    },
    {
        'student_id': '2019-2-60-015',
        'name': 'Nusrat Maisha',
        'gender': 'female',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
    },
    {
        'student_id': '2019-2-60-025',
        'name': 'Md. Tanvir Mobasshir',
        'gender': 'male',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk
    },
    {
        'student_id': '2018-2-60-127',
        'name': 'A. K. M. Sadat',
        'gender': 'male',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk
    },
    {
        'student_id': '2020-1-60-226',
        'name': 'Sofia Noor Rafa',
        'gender': 'female',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
    },
    {
        'student_id': '2020-1-65-001',
        'name': 'Komol Kunty Rajib',
        'gender': 'male',
        'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
        'username_id': User.objects.get(username='2020-1-65-001').pk
    },
    {
        'student_id': 'admin',
        'name': 'admin',
        'gender': 'male',
        'advisor_id': Faculty.objects.get(faculty_id='admin').pk,
        'username_id': User.objects.get(username='admin').pk
    }
]

for i in students:
    r = Student(**i)
    r.save()
