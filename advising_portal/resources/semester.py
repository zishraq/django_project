from django.contrib.auth.models import User
from django.utils import timezone

from advising_portal.models import Semester

import datetime

semesters = [
    {
        'semester_id': 1,
        'semester_name': 'Summer-2018',
        'semester_starts_at': datetime.datetime(year=2018, month=5, day=4),
        'semester_ends_at': datetime.datetime(year=2018, month=8, day=18),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 2,
        'semester_name': 'Fall-2018',
        'semester_starts_at': datetime.datetime(year=2018, month=9, day=1),
        'semester_ends_at': datetime.datetime(year=2018, month=12, day=17),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 3,
        'semester_name': 'Spring-2019',
        'semester_starts_at': datetime.datetime(year=2019, month=1, day=3),
        'semester_ends_at': datetime.datetime(year=2019, month=4, day=20),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 4,
        'semester_name': 'Summer-2019',
        'semester_starts_at': datetime.datetime(year=2019, month=5, day=4),
        'semester_ends_at': datetime.datetime(year=2019, month=8, day=18),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 5,
        'semester_name': 'Fall-2019',
        'semester_starts_at': datetime.datetime(year=2019, month=9, day=1),
        'semester_ends_at': datetime.datetime(year=2019, month=12, day=17),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 6,
        'semester_name': 'Spring-2020',
        'semester_starts_at': datetime.datetime(year=2020, month=1, day=3),
        'semester_ends_at': datetime.datetime(year=2020, month=4, day=20),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 7,
        'semester_name': 'Summer-2020',
        'semester_starts_at': datetime.datetime(year=2020, month=5, day=7),
        'semester_ends_at': datetime.datetime(year=2020, month=8, day=15),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 8,
        'semester_name': 'Fall-2020',
        'semester_starts_at': datetime.datetime(year=2020, month=9, day=6),
        'semester_ends_at': datetime.datetime(year=2020, month=12, day=17),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 9,
        'semester_name': 'Spring-2021',
        'semester_starts_at': datetime.datetime(year=2021, month=1, day=9),
        'semester_ends_at': datetime.datetime(year=2021, month=4, day=19),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 10,
        'semester_name': 'Summer-2021',
        'semester_starts_at': datetime.datetime(year=2021, month=5, day=12),
        'semester_ends_at': datetime.datetime(year=2021, month=8, day=24),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 11,
        'semester_name': 'Fall-2021',
        'semester_starts_at': datetime.datetime(year=2021, month=9, day=9),
        'semester_ends_at': datetime.datetime(year=2021, month=12, day=19),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': False
    },
    {
        'semester_id': 12,
        'semester_name': 'Spring-2022',
        'semester_starts_at': datetime.datetime(year=2022, month=2, day=6),
        'semester_ends_at': datetime.datetime(year=2022, month=5, day=18),
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'advising_status': True,
        'is_active': True
    }
]

for i in semesters:
    r = Semester(**i)
    r.save()
