"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_wsgi_application()


# if __name__ == '__main__':
#     from advising_portal.models import RoutineSlot, TimeSlot, Department, Course, Faculty, Section, Student, Semester
#     from django.contrib.auth.models import User
#     import datetime
#     from django.utils import timezone
#
#     users = [
#         {
#             'username': 'ishraq',
#             'email': 'ishraq@gmail.com',
#             'password1': '123456Seven',
#             'password2': '123456Seven'
#         },
#         {
#             'username': 'amit',
#             'email': 'ami@gmail.com',
#             'password1': '123456Seven',
#             'password2': '123456Seven'
#         },
#         {
#             'username': 'tuhin',
#             'email': 'tuhin@gmail.com',
#             'password1': '123456Seven',
#             'password2': '123456Seven'
#         },
#         {
#             'username': 'alex',
#             'email': 'alex@gmail.com',
#             'password1': '123456Seven',
#             'password2': '123456Seven'
#         }
#     ]
#
#     departments = [
#         {
#             'department_id': 'CSE',
#             'department_name': 'Computer Science and Engineering',
#             'created_at': timezone.now(),
#             'created_by': User.objects.get(username='admin')
#         }
#     ]
#
#     for i in departments:
#         r = Department(**i)
#         r.save()
#
#     semesters = [
#         {
#             'semester_id': 'Summer 2022',
#             'semester_starts_on': datetime.datetime(year=2022, month=2, day=1),
#             'semester_ends_on': datetime.datetime(year=2022, month=5, day=18),
#             'created_at': timezone.now(),
#             'created_by': User.objects.get(username='admin'),
#             'advising_status': True
#         }
#     ]
#
#     for i in semesters:
#         r = Semester(**i)
#         r.save()
#
#     courses = [
#         {
#             'course_id': 'CSE103',
#             'course_code': 'CSE103',
#             'course_title': 'Structured Programming',
#             'department_id': Department.objects.get(pk='CSE'),
#             'prerequisite_course_id': None,
#             'credit': 3,
#             'created_by': User.objects.get(username='admin')
#         },
#         {
#             'course_id': 'CSE110',
#             'course_code': 'CSE110',
#             'course_title': 'Object Oriented Programming',
#             'department_id': Department.objects.get(pk='CSE'),
#             'prerequisite_course_id': None,
#             'credit': 3,
#             'created_by': User.objects.get(username='admin')
#         }
#     ]
#
#     for i in courses:
#         r = Course(**i)
#         r.save()
#
#     faculties = [
#         {
#             'faculty_id': 'RDA',
#             'name': 'Rashedul Amin Tuhin',
#             'initials': 'RDA',
#             'user_id': User.objects.get(username='tuhin')
#         },
#         {
#             'faculty_id': 'AKD',
#             'name': 'Amit Kumar Das',
#             'initials': 'AKD',
#             'user_id': User.objects.get(username='amit')
#         }
#     ]
#
#     for i in faculties:
#         r = Faculty(**i)
#         r.save()
#
#     routine_slot = [
#         {
#             'routine_id': 'S01T01'
#         },
#         {
#             'routine_id': 'S01T01'
#         },
#         {
#             'routine_id': 'S02T02'
#         },
#         {
#             'routine_id': 'S02T02'
#         },
#         {
#             'routine_id': 'S03T03'
#         },
#         {
#             'routine_id': 'S03T03'
#         },
#         {
#             'routine_id': 'S04T04'
#         },
#         {
#             'routine_id': 'S04T04'
#         },
#         {
#             'routine_id': 'S04T04'
#         },
#         {
#             'routine_id': 'S04T04'
#         },
#         {
#             'routine_id': 'S05T05'
#         },
#         {
#             'routine_id': 'S05T05'
#         },
#         {
#             'routine_id': 'M01W01'
#         },
#         {
#             'routine_id': 'M01W01'
#         },
#         {
#             'routine_id': 'M02W02'
#         },
#         {
#             'routine_id': 'M02W02'
#         },
#         {
#             'routine_id': 'M03W03'
#         },
#         {
#             'routine_id': 'M03W03'
#         },
#         {
#             'routine_id': 'M04W04'
#         },
#         {
#             'routine_id': 'M04W04'
#         },
#         {
#             'routine_id': 'M04W04'
#         },
#         {
#             'routine_id': 'M04W04'
#         },
#         {
#             'routine_id': 'M05W05'
#         },
#         {
#             'routine_id': 'M05W05'
#         }
#     ]
#
#     time_slots = {
#         'S01': {
#             'time_slot_id': 'S01',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'S02': {
#             'time_slot_id': 'S02',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
#         },
#         'S03': {
#             'time_slot_id': 'S03',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=20, second=0).time()
#         },
#         'S04': {
#             'time_slot_id': 'S04',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=0, second=0).time()
#         },
#         'S05': {
#             'time_slot_id': 'S05',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=40, second=0).time()
#         },
#         'S06': {
#             'time_slot_id': 'S06',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'S07': {
#             'time_slot_id': 'S07',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
#         },
#         'S08': {
#             'time_slot_id': 'S08',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30, second=0).time()
#         },
#         'S09': {
#             'time_slot_id': 'S09',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=6, minute=50, second=0).time()
#         },
#         'S10': {
#             'time_slot_id': 'S10',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=0, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=0, second=0).time()
#         },
#         'S11': {
#             'time_slot_id': 'S11',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=2, minute=50, second=0).time()
#         },
#         'S12': {
#             'time_slot_id': 'S12',
#             'day': 'S',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=7, minute=50, second=0).time()
#         },
#         'M01': {
#             'time_slot_id': 'M01',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'M02': {
#             'time_slot_id': 'M02',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
#         },
#         'M03': {
#             'time_slot_id': 'M03',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=20, second=0).time()
#         },
#         'M04': {
#             'time_slot_id': 'M04',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=0, second=0).time()
#         },
#         'M05': {
#             'time_slot_id': 'M05',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=40, second=0).time()
#         },
#         'M06': {
#             'time_slot_id': 'M06',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'M07': {
#             'time_slot_id': 'M07',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
#         },
#         'M08': {
#             'time_slot_id': 'M08',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30, second=0).time()
#         },
#         'M09': {
#             'time_slot_id': 'M09',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=6, minute=50, second=0).time()
#         },
#         'M10': {
#             'time_slot_id': 'M10',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=0, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=0, second=0).time()
#         },
#         'M11': {
#             'time_slot_id': 'M11',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=2, minute=50, second=0).time()
#         },
#         'M12': {
#             'time_slot_id': 'M12',
#             'day': 'M',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=7, minute=50, second=0).time()
#         },
#         'T01': {
#             'time_slot_id': 'T01',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'T02': {
#             'time_slot_id': 'T02',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
#         },
#         'T03': {
#             'time_slot_id': 'T03',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=20, second=0).time()
#         },
#         'T04': {
#             'time_slot_id': 'T04',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=0, second=0).time()
#         },
#         'T05': {
#             'time_slot_id': 'T05',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=40, second=0).time()
#         },
#         'T06': {
#             'time_slot_id': 'T06',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'T07': {
#             'time_slot_id': 'T07',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
#         },
#         'T08': {
#             'time_slot_id': 'T08',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30, second=0).time()
#         },
#         'T09': {
#             'time_slot_id': 'T09',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=6, minute=50, second=0).time()
#         },
#         'T10': {
#             'time_slot_id': 'T10',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=0, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=0, second=0).time()
#         },
#         'T11': {
#             'time_slot_id': 'T11',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=2, minute=50, second=0).time()
#         },
#         'T12': {
#             'time_slot_id': 'T12',
#             'day': 'T',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=7, minute=50, second=0).time()
#         },
#         'W01': {
#             'time_slot_id': 'W01',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'W02': {
#             'time_slot_id': 'W02',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
#         },
#         'W03': {
#             'time_slot_id': 'W03',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=20, second=0).time()
#         },
#         'W04': {
#             'time_slot_id': 'W04',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=0, second=0).time()
#         },
#         'W05': {
#             'time_slot_id': 'W05',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=40, second=0).time()
#         },
#         'W06': {
#             'time_slot_id': 'W06',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'W07': {
#             'time_slot_id': 'W07',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
#         },
#         'W08': {
#             'time_slot_id': 'W08',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30, second=0).time()
#         },
#         'W09': {
#             'time_slot_id': 'W09',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=6, minute=50, second=0).time()
#         },
#         'W10': {
#             'time_slot_id': 'W10',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=0, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=0, second=0).time()
#         },
#         'W11': {
#             'time_slot_id': 'W11',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=2, minute=50, second=0).time()
#         },
#         'W12': {
#             'time_slot_id': 'W12',
#             'day': 'W',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=7, minute=50, second=0).time()
#         },
#         'R01': {
#             'time_slot_id': 'R01',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'R02': {
#             'time_slot_id': 'R02',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
#         },
#         'R03': {
#             'time_slot_id': 'R03',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=20, second=0).time()
#         },
#         'R04': {
#             'time_slot_id': 'R04',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=0, second=0).time()
#         },
#         'R05': {
#             'time_slot_id': 'R05',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=40, second=0).time()
#         },
#         'R06': {
#             'time_slot_id': 'R06',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
#         },
#         'R07': {
#             'time_slot_id': 'R07',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
#         },
#         'R08': {
#             'time_slot_id': 'R08',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30, second=0).time()
#         },
#         'R09': {
#             'time_slot_id': 'R09',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=6, minute=50, second=0).time()
#         },
#         'R10': {
#             'time_slot_id': 'R10',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=0, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=0, second=0).time()
#         },
#         'R11': {
#             'time_slot_id': 'R11',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=2, minute=50, second=0).time()
#         },
#         'R12': {
#             'time_slot_id': 'R12',
#             'day': 'R',
#             'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
#             'end_time': datetime.datetime(year=2020, month=1, day=1, hour=7, minute=50, second=0).time()
#         }
#     }
#
#     for i in routine_slot:
#         r = RoutineSlot(**i)
#         r.save()
#
#         n = len(i['routine_id'])
#
#         for x in range(0, n, 3):
#             get_time_slot = time_slots[i['routine_id'][x:x + 3]]
#             get_time_slot['routine_id'] = RoutineSlot.objects.get(pk=i['routine_id'])
#
#             t = TimeSlot(**get_time_slot)
#             t.save()
#
#     sections = [
#         {
#             'section_id': 'CSE1031',
#             'section_no': 1,
#             'section_capacity': 30,
#             'total_students': 0,
#             'instructor_id': Faculty.objects.get(pk='AKD'),
#             'routine_id': RoutineSlot.objects.get(pk='S01T01'),
#             'course_id': Course.objects.get(pk='CSE103'),
#         },
#         {
#             'section_id': 'CSE1032',
#             'section_no': 2,
#             'section_capacity': 30,
#             'total_students': 0,
#             'instructor_id': Faculty.objects.get(pk='RDA'),
#             'routine_id': RoutineSlot.objects.get(pk='M01W01'),
#             'course_id': Course.objects.get(pk='CSE103'),
#         },
#         {
#             'section_id': 'CSE1101',
#             'section_no': 1,
#             'section_capacity': 30,
#             'total_students': 0,
#             'instructor_id': Faculty.objects.get(pk='RDA'),
#             'routine_id': RoutineSlot.objects.get(pk='S01T01'),
#             'course_id': Course.objects.get(pk='CSE110'),
#         },
#         {
#             'section_id': 'CSE1102',
#             'section_no': 2,
#             'section_capacity': 30,
#             'total_students': 0,
#             'instructor_id': Faculty.objects.get(pk='AKD'),
#             'routine_id': RoutineSlot.objects.get(pk='M01W01'),
#             'course_id': Course.objects.get(pk='CSE110'),
#         }
#     ]
#
#     students = [
#         {
#             'student_id': '2019-2-60-022',
#             'name': 'Alex Steiner',
#             'advisor': Faculty.objects.get(faculty_id='AKD'),
#             'user_id': User.objects.get(username='alex')
#         },
#         {
#             'student_id': '2019-2-60-021',
#             'name': 'Zuhair Ishraq Zareef',
#             'advisor': Faculty.objects.get(faculty_id='RDA'),
#             'user_id': User.objects.get(username='ishraq')
#         },
#         {
#             'student_id': 'admin',
#             'name': 'admin',
#             'advisor': Faculty.objects.get(faculty_id='RDA'),
#             'user_id': User.objects.get(username='admin')
#         }
#     ]
#
#     for i in sections:
#         r = Section(**i)
#         r.save()
#
#     for i in students:
#         r = Student(**i)
#         r.save()
