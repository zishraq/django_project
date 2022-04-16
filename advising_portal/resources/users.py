from django.contrib.auth.models import User


users = [
    {
        'username': 'admin',
        'password': 'admin',
        'is_superuser': True
    },
    {
        'username': '2020-1-65-001',
        'password': '123456Seven',
    },
    {
        'username': 'amit',
        'password': '123456Seven',
    },
    {
        'username': 'tuhin',
        'password': '123456Seven',
    }
]

for u in users:
    user = User.objects.create_user(**u)
    user.save()
