from django.contrib.auth.models import User
from advising_portal.models import Faculty


faculties = [
    {
        'faculty_id': 'ZI',
        'name': 'Zuhair Ishraq',
        'initials': 'ZI',
        'gender': 'male',
        'username_id': User.objects.get(username='ishraq').pk
    },
    {
        'faculty_id': 'NM',
        'name': 'Nusrat Maisha',
        'initials': 'NM',
        'gender': 'male',
        'username_id': User.objects.get(username='nusrat').pk
    },
    {
        'faculty_id': 'TM',
        'name': 'Tanvir Mobasshir',
        'initials': 'TM',
        'gender': 'male',
        'username_id': User.objects.get(username='tanvir').pk
    },
    {
        'faculty_id': 'RR',
        'name': 'Rajib Raiyat',
        'initials': 'RR',
        'gender': 'male',
        'username_id': User.objects.get(username='rajib').pk
    },
    {
        'faculty_id': 'AKMS',
        'name': 'AKM Sadat',
        'initials': 'AKMS',
        'gender': 'male',
        'username_id': User.objects.get(username='sadat').pk
    },
    {
        'faculty_id': 'admin',
        'name': 'admin',
        'initials': 'admin',
        'gender': 'male',
        'username_id': User.objects.get(username='admin').pk
    }
]
