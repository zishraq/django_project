from django.contrib.auth.models import User
from django.utils import timezone

from advising_portal.models import Department

import datetime


departments = [
    {
        'department_id': 'CSE',
        'department_name': 'Computer Science and Engineering',
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'chairman_id': User.objects.get(username='nusrat').pk
    },
    {
        'department_id': 'GEN',
        'department_name': 'General',
        'created_at': timezone.now(),
        'created_by_id': User.objects.get(username='admin').pk,
        'chairman_id': User.objects.get(username='tanvir').pk
    }
]
