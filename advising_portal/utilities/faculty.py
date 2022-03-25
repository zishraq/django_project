from django.contrib.auth.models import User
from advising_portal.models import Faculty


faculties = [
    {
        'faculty_id': 'RDA',
        'name': 'Rashedul Amin Tuhin',
        'initials': 'RDA',
        'username_id': User.objects.get(username='tuhin').pk
    },
    {
        'faculty_id': 'AKD',
        'name': 'Amit Kumar Das',
        'initials': 'AKD',
        'username_id': User.objects.get(username='amit').pk
    }
]

for i in faculties:
    r = Faculty(**i)
    r.save()
