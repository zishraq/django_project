from django.contrib.auth.models import User

from advising_portal.models import Faculty

students = [
    {
        'student_id': '2019-2-60-022',
        'name': 'Alex Steiner',
        'advisor': Faculty.objects.get(faculty_id='AKD'),
        'user_id': User.objects.get(username='alex')
    }
]
