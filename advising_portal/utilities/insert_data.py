from advising_portal.models import RoutineSlot, TimeSlot, Department, Course, Faculty, Section, Student
from advising_portal.utilities.course import courses
from advising_portal.utilities.department import departments
from advising_portal.utilities.faculty import faculties
from advising_portal.utilities.routine import routine_slot
from advising_portal.utilities.section import sections
from advising_portal.utilities.student import students
from advising_portal.utilities.time_slot import time_slots


def insert_data():
    for i in routine_slot:
        r = RoutineSlot(**i)
        r.save()

        n = len(i['routine_id'])

        for x in range(0, n, 3):
            get_time_slot = time_slots[i['routine_id'][x:x + 3]]
            get_time_slot['routine_id'] = RoutineSlot.objects.get(pk=i['routine_id'])

            t = TimeSlot(**get_time_slot)
            t.save()

    for i in departments:
        r = Department(**i)
        r.save()

    for i in courses:
        r = Course(**i)
        r.save()

    for i in faculties:
        r = Faculty(**i)
        r.save()

    for i in sections:
        r = Section(**i)
        r.save()

    for i in students:
        r = Student(**i)
        r.save()


if __name__ == '__main__':
    insert_data()
