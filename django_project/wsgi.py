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


if __name__ == '__main__':
    from advising_portal.models import RoutineSlot, TimeSlot, RoutineAndTime, Department, Course, Faculty, Section, Student, Semester
    from django.contrib.auth.models import User
    import datetime
    from django.utils import timezone

    departments = [
        {
            'department_id': 'CSE',
            'department_name': 'Computer Science and Engineering',
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'department_id': 'GEN',
            'department_name': 'General',
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk
        }
    ]

    for i in departments:
        r = Department(**i)
        r.save()

    semesters = [
        {
            'semester_id': 1,
            'semester_name': 'Summer 2019',
            'semester_starts_on': datetime.datetime(year=2019, month=5, day=4),
            'semester_ends_on': datetime.datetime(year=2019, month=8, day=18),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 2,
            'semester_name': 'Fall 2019',
            'semester_starts_on': datetime.datetime(year=2019, month=9, day=1),
            'semester_ends_on': datetime.datetime(year=2019, month=12, day=17),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 3,
            'semester_name': 'Spring 2020',
            'semester_starts_on': datetime.datetime(year=2020, month=1, day=3),
            'semester_ends_on': datetime.datetime(year=2020, month=4, day=20),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 4,
            'semester_name': 'Summer 2020',
            'semester_starts_on': datetime.datetime(year=2020, month=5, day=7),
            'semester_ends_on': datetime.datetime(year=2020, month=8, day=15),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 5,
            'semester_name': 'Fall 2020',
            'semester_starts_on': datetime.datetime(year=2020, month=9, day=6),
            'semester_ends_on': datetime.datetime(year=2020, month=12, day=17),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 6,
            'semester_name': 'Spring 2021',
            'semester_starts_on': datetime.datetime(year=2021, month=1, day=9),
            'semester_ends_on': datetime.datetime(year=2021, month=4, day=19),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 7,
            'semester_name': 'Summer 2021',
            'semester_starts_on': datetime.datetime(year=2021, month=5, day=12),
            'semester_ends_on': datetime.datetime(year=2021, month=8, day=24),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 8,
            'semester_name': 'Fall 2021',
            'semester_starts_on': datetime.datetime(year=2021, month=9, day=9),
            'semester_ends_on': datetime.datetime(year=2021, month=12, day=19),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 9,
            'semester_name': 'Spring 2022',
            'semester_starts_on': datetime.datetime(year=2022, month=2, day=6),
            'semester_ends_on': datetime.datetime(year=2022, month=5, day=18),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': True
        },
    ]

    for i in semesters:
        r = Semester(**i)
        r.save()

    courses = [
        {
            'course_id': 'CSE103',
            'course_code': 'CSE103',
            'course_title': 'Structured Programming',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': None,
            'credit': 4.5,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE106',
            'course_code': 'CSE106',
            'course_title': 'Discrete Mathematics',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': 'CSE103',
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE110',
            'course_code': 'CSE110',
            'course_title': 'Object Oriented Programming',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': "CSE106",
            'credit': 4.5,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE200',
            'course_code': 'CSE200',
            'course_title': 'Computer-Aided Engineering Drawing',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': None,
            'credit': 1,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE246',
            'course_code': 'CSE246',
            'course_title': 'Algorithms',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': None,
            'credit': 4.5,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE207',
            'course_code': 'CSE207',
            'course_title': 'Data Structures',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': "CSE110",
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE302',
            'course_code': 'CSE302',
            'course_title': 'Database Systems',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': "CSE106",
            'credit': 4.5,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE325',
            'course_code': 'CSE325',
            'course_title': 'Operating Systems',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': "CSE207",
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE345',
            'course_code': 'CSE345',
            'course_title': 'Digital Logic Design',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': None,
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE347',
            'course_code': 'CSE347',
            'course_title': 'Information System Analysis and Design',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': "CSE302",
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE360',
            'course_code': 'CSE360',
            'course_title': 'Computer Architecture',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': 'CSE325',
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE405',
            'course_code': 'CSE405',
            'course_title': 'Computer Networks',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': 'CSE246',
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'ENG101',
            'course_code': 'ENG101',
            'course_title': 'Basic English',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': None,
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'ENG102',
            'course_code': 'ENG102',
            'course_title': 'Composition and Communication Skills',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "ENG101",
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'GEN226',
            'course_code': 'GEN226',
            'course_title': 'Emergence of Bangladesh',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': 'ENG102',
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'ECO101',
            'course_code': 'ECO101',
            'course_title': 'Principle of Microeconomics',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        }, {
            'course_id': 'GEN203',
            'course_code': 'GEN203',
            'course_title': 'Ecological System and Environment',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'GEN214',
            'course_code': 'GEN214',
            'course_title': 'Development Studies',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "ENG102",
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'GEN210',
            'course_code': 'GEN210',
            'course_title': 'International Relation',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "ENG102",
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'BUS231',
            'course_code': 'BUS231',
            'course_title': 'Business Communication',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "ENG102",
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'PHY109',
            'course_code': 'PHY109',
            'course_title': 'Engineering Physics-I (Introductory Classical Physics)',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'PHY209',
            'course_code': 'PHY209',
            'course_title': 'Engineering Physics-II (Introductory Quantum Physics)',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        }
    ]

    for i in courses:
        r = Course(**i)
        r.save()

    faculties = [
        {
            'faculty_id': 'RDA',
            'name': 'Rashedul Amin Tuhin',
            'initials': 'RDA',
            'username_id': User.objects.get(username='tuhin').pk
        },
        {
            'faculty_id': 'AKD',
            'name': 'Amit Kumar Das',
            'initials': 'AKD',
            'username_id': User.objects.get(username='amit').pk
        },
        {
            'faculty_id': 'admin',
            'name': 'admin',
            'initials': 'admin',
            'username_id': User.objects.get(username='admin').pk
        }
    ]

    for i in faculties:
        r = Faculty(**i)
        r.save()

    time_slots = {
        'S01': {
            'time_slot_id': 'S01',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'S02': {
            'time_slot_id': 'S02',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
        },
        'S03': {
            'time_slot_id': 'S03',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
        },
        'S04': {
            'time_slot_id': 'S04',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
        },
        'S05': {
            'time_slot_id': 'S05',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
        },
        'S06': {
            'time_slot_id': 'S06',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'S07': {
            'time_slot_id': 'S07',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
        },
        'S08': {
            'time_slot_id': 'S08',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
        },
        'S09': {
            'time_slot_id': 'S09',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
        },
        'S10': {
            'time_slot_id': 'S10',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
        },
        'S11': {
            'time_slot_id': 'S11',
            'day': 'S',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
        },
        'M01': {
            'time_slot_id': 'M01',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'M02': {
            'time_slot_id': 'M02',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
        },
        'M03': {
            'time_slot_id': 'M03',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
        },
        'M04': {
            'time_slot_id': 'M04',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
        },
        'M05': {
            'time_slot_id': 'M05',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
        },
        'M06': {
            'time_slot_id': 'M06',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'M07': {
            'time_slot_id': 'M07',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
        },
        'M08': {
            'time_slot_id': 'M08',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
        },
        'M09': {
            'time_slot_id': 'M09',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
        },
        'M10': {
            'time_slot_id': 'M10',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
        },
        'M11': {
            'time_slot_id': 'M11',
            'day': 'M',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
        },
        'T01': {
            'time_slot_id': 'T01',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'T02': {
            'time_slot_id': 'T02',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
        },
        'T03': {
            'time_slot_id': 'T03',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
        },
        'T04': {
            'time_slot_id': 'T04',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
        },
        'T05': {
            'time_slot_id': 'T05',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
        },
        'T06': {
            'time_slot_id': 'T06',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'T07': {
            'time_slot_id': 'T07',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
        },
        'T08': {
            'time_slot_id': 'T08',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
        },
        'T09': {
            'time_slot_id': 'T09',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
        },
        'T10': {
            'time_slot_id': 'T10',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
        },
        'T11': {
            'time_slot_id': 'T11',
            'day': 'T',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
        },
        'W01': {
            'time_slot_id': 'W01',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'W02': {
            'time_slot_id': 'W02',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
        },
        'W03': {
            'time_slot_id': 'W03',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
        },
        'W04': {
            'time_slot_id': 'W04',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
        },
        'W05': {
            'time_slot_id': 'W05',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
        },
        'W06': {
            'time_slot_id': 'W06',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'W07': {
            'time_slot_id': 'W07',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
        },
        'W08': {
            'time_slot_id': 'W08',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
        },
        'W09': {
            'time_slot_id': 'W09',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
        },
        'W10': {
            'time_slot_id': 'W10',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
        },
        'W11': {
            'time_slot_id': 'W11',
            'day': 'W',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
        },
        'R01': {
            'time_slot_id': 'R01',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'R02': {
            'time_slot_id': 'R02',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
        },
        'R03': {
            'time_slot_id': 'R03',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
        },
        'R04': {
            'time_slot_id': 'R04',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
        },
        'R05': {
            'time_slot_id': 'R05',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
        },
        'R06': {
            'time_slot_id': 'R06',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
        },
        'R07': {
            'time_slot_id': 'R07',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
        },
        'R08': {
            'time_slot_id': 'R08',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
        },
        'R09': {
            'time_slot_id': 'R09',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
        },
        'R10': {
            'time_slot_id': 'R10',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
        },
        'R11': {
            'time_slot_id': 'R11',
            'day': 'R',
            'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
            'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
        }
    }

    for i in time_slots.values():
        t = TimeSlot(**i)
        t.save()

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
            'routine_id': 'S01T01R09'
        },
        {
            'routine_id': 'S01R01'
        },
        {
            'routine_id': 'S02R02'
        },
        {
            'routine_id': 'S03R03'
        },
        {
            'routine_id': 'S04R04'
        },
        {
            'routine_id': 'S05R05'
        },
        {
            'routine_id': 'S01R01R09'
        },
        {
            'routine_id': 'T01R01'
        },
        {
            'routine_id': 'T02R02'
        },
        {
            'routine_id': 'T03R03'
        },
        {
            'routine_id': 'T04R04'
        },
        {
            'routine_id': 'T05R05'
        },
        {
            'routine_id': 'T01R01R09'
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
        },
        {
            'routine_id': 'M01W01W09'
        }
    ]

    c = 1

    for i in routine_slot:
        r = RoutineSlot(**i)
        r.save()

        routine_id = i['routine_id']
        selected_routine_slot_chunks = [routine_id[i:i + 3] for i in range(0, len(routine_id), 3)]

        for chunk in selected_routine_slot_chunks:
            routine_data = {
                'routine_slot_id': routine_id,
                'time_slot_id': chunk
            }

            rt = RoutineAndTime(**routine_data)
            rt.save()

    sections = [
        {
            'section_id': 'CSE1031',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': 'AKD',
            'routine_id': 'M01W01W09',
            'course_id': 'CSE103',
        },
        {
            'section_id': 'CSE1061',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='RDA').pk,
            'routine_id': RoutineSlot.objects.get(pk='S01T01').pk,
            'course_id': Course.objects.get(pk='CSE103').pk,
        },
        {
            'section_id': 'CSE1101',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='RDA').pk,
            'routine_id': RoutineSlot.objects.get(pk='S02T02').pk,
            'course_id': Course.objects.get(pk='CSE110').pk,
        },
        {
            'section_id': 'CSE2001',
            'section_no': 1,
            'section_capacity': 40,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='AKD').pk,
            'routine_id': RoutineSlot.objects.get(pk='S03T03').pk,
            'course_id': Course.objects.get(pk='CSE200').pk,
        },
        {
            'section_id': 'CSE2461',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='RDA').pk,
            'routine_id': RoutineSlot.objects.get(pk='S04T04').pk,
            'course_id': Course.objects.get(pk='CSE246').pk,
        },
        {
            'section_id': 'CSE2071',
            'section_no': 1,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='AKD').pk,
            'routine_id': RoutineSlot.objects.get(pk='M01W01').pk,
            'course_id': Course.objects.get(pk='CSE207').pk,
        },
        {
            'section_id': 'CSE3021',
            'section_no': 1,
            'section_capacity': 40,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='AKD').pk,
            'routine_id': RoutineSlot.objects.get(pk='M03W03').pk,
            'course_id': Course.objects.get(pk='CSE302').pk,
        },
        {
            'section_id': 'CSE3251',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='RDA').pk,
            'routine_id': RoutineSlot.objects.get(pk='M01W01').pk,
            'course_id': Course.objects.get(pk='CSE325').pk,
        },
        {
            'section_id': 'CSE3451',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='AKD').pk,
            'routine_id': RoutineSlot.objects.get(pk='S01R01').pk,
            'course_id': Course.objects.get(pk='CSE345').pk,
        },
        {
            'section_id': 'CSE3471',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='RDA').pk,
            'routine_id': RoutineSlot.objects.get(pk='T02R02').pk,
            'course_id': Course.objects.get(pk='CSE347').pk,
        },
        {
            'section_id': 'CSE3601',
            'section_no': 1,
            'section_capacity': 45,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='AKD').pk,
            'routine_id': RoutineSlot.objects.get(pk='T04R04').pk,
            'course_id': Course.objects.get(pk='CSE360').pk,
        },
        {
            'section_id': 'ENG1011',
            'section_no': 1,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='RDA').pk,
            'routine_id': RoutineSlot.objects.get(pk='T05R05').pk,
            'course_id': Course.objects.get(pk='ENG101').pk,
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
            'section_id': 'ENG1021',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': Faculty.objects.get(pk='AKD').pk,
            'routine_id': RoutineSlot.objects.get(pk='S05R05').pk,
            'course_id': Course.objects.get(pk='ENG102').pk,
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
            'routine_id': RoutineSlot.objects.get(pk='T04R04').pk,
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
            'routine_id': RoutineSlot.objects.get(pk='S01R01R09').pk,
            'course_id': Course.objects.get(pk='PHY209').pk,
        }
    ]

    for i in sections:
        r = Section(**i)
        r.save()

    students = [
        {
            'student_id': '2019-2-60-022',
            'name': 'Alex Steiner',
            'advisor_id': Faculty.objects.get(faculty_id='AKD').pk,
            'username_id': User.objects.get(username='alex').pk
        },
        {
            'student_id': '2019-2-60-021',
            'name': 'Zuhair Ishraq Zareef',
            'advisor_id': Faculty.objects.get(faculty_id='RDA').pk,
            'username_id': User.objects.get(username='ishraq').pk
        }
    ]

    for i in students:
        r = Student(**i)
        r.save()
