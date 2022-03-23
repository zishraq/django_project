from django.contrib.auth.models import User
from advising_portal.models import Faculty


faculties = [
    {
        'faculty_id': 'RDA',
        'name': 'Rashedul Amin Tuhin',
        'initials': 'RDA',
        'user_id': User.objects.get(username='tuhin')
    },
    {
        'faculty_id': 'AKD',
        'name': 'Amit Kumar Das',
        'initials': 'AKD',
        'user_id': User.objects.get(username='amit')
    }
]

for i in faculties:
    r = Faculty(**i)
    r.save()
