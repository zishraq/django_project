import datetime

from django.contrib.auth.models import User
from advising_portal.models import Faculty

from random import randrange
from datetime import timedelta, datetime

from users.send_otp import generate_otp


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


faculties = [
    {
        'faculty_id': 'ZI',
        'name': 'Zuhair Ishraq',
        'initials': 'ZI',
        'gender': 'male',
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'username_id': User.objects.get(username='ishraq').pk
    },
    {
        'faculty_id': 'NM',
        'name': 'Nusrat Maisha',
        'initials': 'NM',
        'gender': 'male',
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'username_id': User.objects.get(username='nusrat').pk
    },
    {
        'faculty_id': 'TM',
        'name': 'Tanvir Mobasshir',
        'initials': 'TM',
        'gender': 'male',
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'username_id': User.objects.get(username='tanvir').pk
    },
    {
        'faculty_id': 'admin',
        'name': 'admin',
        'initials': 'admin',
        'gender': 'male',
        'date_of_birth': random_date(datetime(1998, 1, 1), datetime.now()).date(),
        'address': generate_otp(),
        'username_id': User.objects.get(username='admin').pk
    }
]
