from django.contrib.auth.models import User

from advising_portal.models import Department

import datetime


departments = [
    {
        'department_id': 'CSE',
        'department_name': 'Computer Science and Engineering',
        'credit': 3,
        'created_at': datetime.datetime.now(),
        'created_by': User.objects.get(username='admin')
    }
]

for i in departments:
    r = Department(**i)
    r.save()
