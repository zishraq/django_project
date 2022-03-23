import datetime
import uuid
from advising_portal.models import RoutineSlot, TimeSlot, Department, Course, Faculty, Section
from advising_portal.utilities.time_slot import time_slots
from django.contrib.auth.models import User

# str(uuid.uuid4())

routine_slot = [
    {
        'routine_id': 'S01T01'
    },
    {
        'routine_id': 'S02T02'
    },
    {
        'routine_id': 'S03T03'
    },
    {
        'routine_id': 'S04T04'
    },
    {
        'routine_id': 'S05T05'
    },
    {
        'routine_id': 'M01W01'
    },
    {
        'routine_id': 'M02W02'
    },
    {
        'routine_id': 'M03W03'
    },
    {
        'routine_id': 'M04W04'
    },
    {
        'routine_id': 'M05W05'
    }
]

for i in routine_slot:
    r = RoutineSlot(**i)
    r.save()

    n = len(i['routine_id'])

    for x in range(0, n, 3):
        get_time_slot = time_slots[i['routine_id'][x:x + 3]]
        get_time_slot['routine_id'] = RoutineSlot.objects.get(pk=i['routine_id'])

        t = TimeSlot(**get_time_slot)
        t.save()

        # print(x)

r = RoutineSlot.objects.get(pk='S01T01')
print(list(r.timeslot_set.all()))
print(dir(RoutineSlot))
