from advising_portal.models import Faculty, RoutineSlot, Course, Section


sections = [
    {
        'section_id': 'CSE1031',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(routine_id='S01T01').pk,
        'course_id': Course.objects.get(pk='CSE103').pk,
    },
    {
        'section_id': 'CSE1032',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(routine_id='M01W01').pk,
        'course_id': Course.objects.get(pk='CSE103').pk,
    },
    {
        'section_id': 'CSE1101',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(routine_id='S01T01').pk,
        'course_id': Course.objects.get(pk='CSE110').pk,
    },
    {
        'section_id': 'CSE1102',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(routine_id='M01W01').pk,
        'course_id': Course.objects.get(pk='CSE110').pk,
    }
]


for i in sections:
    r = Section(**i)
    r.save()
