from django.contrib.auth.models import User

project_users = [
    {
        'username': 'admin',
        'password': 'admin',
        'is_superuser': True,
        'is_staff': True
    },
    {
        'username': '2020-1-65-001',
        'password': '123456Seven'
    },
    {
        'username': '2019-2-60-015',
        'password': '123456Seven'
    },
    {
        'username': '2019-2-60-022',
        'password': '123456Seven'
    },
    {
        'username': '2019-2-60-025',
        'password': '123456Seven'
    },
    {
        'username': '2018-2-60-127',
        'password': '123456Seven'
    },
    {
        'username': '2020-1-60-226',
        'password': '123456Seven'
    },
    {
        'username': 'ishraq',
        'password': '123456Seven'
    },
    {
        'username': 'nusrat',
        'password': '123456Seven'
    },
    {
        'username': 'tanvir',
        'password': '123456Seven'
    },
    {
        'username': 'rajib',
        'password': '123456Seven'
    },
    {
        'username': 'sadat',
        'password': '123456Seven'
    }
]

for u in project_users:
    user = User.objects.create_user(**u)
    user.save()
