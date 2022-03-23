from advising_portal.models import Faculty, RoutineSlot, Course, Section


sections = [
    {
        'section_id': 'CSE1031',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE103'),
    },
    {
        'section_id': 'CSE1032',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE103'),
    },
    {
        'section_id': 'CSE1101',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE110'),
    },
    {
        'section_id': 'CSE1102',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD'),
        'routine_id': RoutineSlot.objects.get(pk='S01T01'),
        'course_id': Course.objects.get(pk='CSE110'),
    }
]

for i in sections:
    r = Section(**i)
    r.save()
