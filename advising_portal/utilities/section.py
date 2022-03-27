from advising_portal.models import Faculty, RoutineSlot, Course, Section


sections = [
    {
        'section_id': 'CSE1031',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W11').pk,
        'course_id': Course.objects.get(pk='CSE103').pk,
    },
    {
        'section_id': 'ENG1011',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03T03').pk,
        'course_id': Course.objects.get(pk='ENG101').pk,
    },
    {
        'section_id': 'CSE1061',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S01T01').pk,
        'course_id': Course.objects.get(pk='CSE106').pk,
    },
    {
        'section_id': 'ENG1021',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03T03').pk,
        'course_id': Course.objects.get(pk='ENG102').pk,
    },
    {
        'section_id': 'MAT1011',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S04T04').pk,
        'course_id': Course.objects.get(pk='MAT101').pk,
    },
    {
        'section_id': 'CSE1062',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S04T04').pk,
        'course_id': Course.objects.get(pk='CSE106').pk,
    },
    {
        'section_id': 'MAT1021',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S04T04').pk,
        'course_id': Course.objects.get(pk='MAT102').pk,
    },
    {
        'section_id': 'CSE1101',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S01R01T11').pk,
        'course_id': Course.objects.get(pk='CSE110').pk,
    },
    {
        'section_id': 'MAT1041',
        'section_no': 1,
        'section_capacity': 35,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01').pk,
        'course_id': Course.objects.get(pk='MAT104').pk,
    },
    {
        'section_id': 'CHE1091',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W06').pk,
        'course_id': Course.objects.get(pk='CHE109').pk,
    },
    {
        'section_id': 'CSE2091',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03R03T06').pk,
        'course_id': Course.objects.get(pk='CSE209').pk,
    },
    {
        'section_id': 'CSE2511',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S01T01R01').pk,
        'course_id': Course.objects.get(pk='CSE251').pk,
    },
    {
        'section_id': 'CSE2001',
        'section_no': 1,
        'section_capacity': 40,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='T01').pk,
        'course_id': Course.objects.get(pk='CSE200').pk,
    },
    {
        'section_id': 'MAT2051',
        'section_no': 1,
        'section_capacity': 40,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03T03').pk,
        'course_id': Course.objects.get(pk='MAT205').pk,
    },
    {
        'section_id': 'GEN2261',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='T03R03').pk,
        'course_id': Course.objects.get(pk='GEN226').pk,
    },
    {
        'section_id': 'ECO1011',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S05R05').pk,
        'course_id': Course.objects.get(pk='ECO101').pk,
    },
    {
        'section_id': 'CSE2461',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W09').pk,
        'course_id': Course.objects.get(pk='CSE246').pk,
    },
    {
        'section_id': 'CSE2071',
        'section_no': 1,
        'section_capacity': 35,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W11').pk,
        'course_id': Course.objects.get(pk='CSE207').pk,
    },
    {
        'section_id': 'CSE4051',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03T03R06').pk,
        'course_id': Course.objects.get(pk='CSE405').pk,
    },
    {
        'section_id': 'CSE3021',
        'section_no': 1,
        'section_capacity': 40,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S01T01R11').pk,
        'course_id': Course.objects.get(pk='CSE302').pk,
    },
    {
        'section_id': 'CSE3251',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W06').pk,
        'course_id': Course.objects.get(pk='CSE325').pk,
    },
    {
        'section_id': 'CSE3451',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S01R01T09').pk,
        'course_id': Course.objects.get(pk='CSE345').pk,
    },
    {
        'section_id': 'STA1021',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='M05W05').pk,
        'course_id': Course.objects.get(pk='STA102').pk,
    },
    {
        'section_id': 'CSE3471',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03T03R09').pk,
        'course_id': Course.objects.get(pk='CSE347').pk,
    },
    {
        'section_id': 'CSE3601',
        'section_no': 1,
        'section_capacity': 45,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W09').pk,
        'course_id': Course.objects.get(pk='CSE360').pk,
    },
    {
        'section_id': 'ENG1012',
        'section_no': 2,
        'section_capacity': 35,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='T05R05').pk,
        'course_id': Course.objects.get(pk='ENG101').pk,
    },
    {
        'section_id': 'ENG1022',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S05R05').pk,
        'course_id': Course.objects.get(pk='ENG102').pk,
    },
    {
        'section_id': 'GEN2031',
        'section_no': 1,
        'section_capacity': 35,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S05T05').pk,
        'course_id': Course.objects.get(pk='GEN203').pk,
    },
    {
        'section_id': 'GEN2141',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01').pk,
        'course_id': Course.objects.get(pk='GEN214').pk,
    },
    {
        'section_id': 'GEN2101',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S03T03').pk,
        'course_id': Course.objects.get(pk='GEN210').pk,
    },
    {
        'section_id': 'BUS2311',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='S02T02').pk,
        'course_id': Course.objects.get(pk='BUS231').pk,
    },
    {
        'section_id': 'PHY1091',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='M01W01W06').pk,
        'course_id': Course.objects.get(pk='PHY109').pk,
    },
    {
        'section_id': 'PHY2091',
        'section_no': 1,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='AKD').pk,
        'routine_id': RoutineSlot.objects.get(pk='T01R01R09').pk,
        'course_id': Course.objects.get(pk='PHY209').pk,
    },
    {
        'section_id': 'PHY2092',
        'section_no': 2,
        'section_capacity': 30,
        'total_students': 0,
        'instructor_id': Faculty.objects.get(pk='RDA').pk,
        'routine_id': RoutineSlot.objects.get(pk='S01R01').pk,
        'course_id': Course.objects.get(pk='PHY209').pk,
    }
]

for i in sections:
    r = Section(**i)
    r.save()
