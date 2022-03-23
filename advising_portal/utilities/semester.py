from django.contrib.auth.models import User

from advising_portal.models import Semester

import datetime

semesters = [
    {
        'semester_id': 'Summer 2022',
        'semester_starts_on': datetime.datetime(year=2022, month=2, day=1),
        'semester_ends_on': datetime.datetime(year=2022, month=5, day=18),
        'credit': 3,
        'created_at': datetime.datetime.now(),
        'created_by': User.objects.get(username='admin'),
        'advising_status': True
    }
]

for i in semesters:
    r = Semester(**i)
    r.save()
