class User():
    class objects:
        @staticmethod
        def get(username):
            return username

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
