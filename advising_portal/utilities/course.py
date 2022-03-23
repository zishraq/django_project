class Department:
    class objects:
        @staticmethod
        def get(pk):
            return pk

class User:
    class objects:
        @staticmethod
        def get(username):
            return username


course = [
    {
        'course_id': 'CSE103',
        'course_code': 'CSE103',
        'course_title': 'Structured Programming',
        'department_id': Department.objects.get(pk='CSE'),
        'prerequisite_course_id': None,
        'credit': 3,
        'created_by': User.objects.get(username='admin')
    },
    {
        'course_id': 'CSE110',
        'course_code': 'CSE110',
        'course_title': 'Object Oriented Programming',
        'department_id': Department.objects.get(pk='CSE'),
        'prerequisite_course_id': None,
        'credit': 3,
        'created_by': User.objects.get(username='admin')
    }
]
