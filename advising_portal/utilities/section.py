class Faculty:
    class objects:
        @staticmethod
        def get(pk):
            return pk

class RoutineSlot:
    class objects:
        @staticmethod
        def get(pk):
            return pk

class Course:
    class objects:
        @staticmethod
        def get(pk):
            return pk


sections = [
    {
        'section_id': '1',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE103'),
    },
    {
        'section_id': '2',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE103'),
    },
    {
        'section_id': '1',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE110'),
    },
    {
        'section_id': '2',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE110'),
    }
]
