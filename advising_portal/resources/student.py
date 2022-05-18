from datetime import datetime

from django.contrib.auth.models import User

from advising_portal.models import Faculty, Student
from advising_portal.resources.faculty import random_date
from users.send_otp import generate_otp


students = [
    {
        'student_id': '2019-2-60-022',
        'name': 'Zuhair Ishraq Zareef',
        'gender': 'male',
        'advisor_id': Faculty.objects.get(faculty_id='ZI').pk,
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        # 'username_id': User.objects.get(username='2019-2-60-022').pk
    },
    {
        'student_id': '2019-2-60-015',
        'name': 'Nusrat Maisha',
        'gender': 'female',
        'advisor_id': Faculty.objects.get(faculty_id='NM').pk,
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'username_id': User.objects.get(username='2019-2-60-015').pk
    },
    {
        'student_id': '2019-2-60-025',
        'name': 'Md. Tanvir Mobasshir',
        'gender': 'male',
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'advisor_id': Faculty.objects.get(faculty_id='TM').pk,
        'username_id': User.objects.get(username='2019-2-60-025').pk
    },
    {
        'student_id': 'admin',
        'name': 'admin',
        'gender': 'male',
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'advisor_id': Faculty.objects.get(faculty_id='admin').pk,
        'username_id': User.objects.get(username='admin').pk
    }
]
