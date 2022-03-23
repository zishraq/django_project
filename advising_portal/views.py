from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student
from django.contrib.auth.decorators import login_required

import datetime


@login_required
def home(request):
    sections = list(Section.objects.all())
    view_data = []

    for section in sections:
        formatted_data = {
            'section_id': section.section_id,
            'section_no': section.section_no,
            'section_capacity': section.section_capacity,
            'total_students': section.total_students,
            'department_name': section.course_id.department_id.department_name,
            'instructor_id': section.instructor_id.name,
            'course_id': section.course_id.course_code,
            'credit': section.course_id.credit,
        }

        routines = {}
        for routine in section.routine_id.timeslot_set.all():
            time_part = str(routine)[2:]
            day_part = str(routine)[0]

            if time_part not in routines:
                routines[time_part] = day_part

            else:
                routines[time_part] += day_part

        routine_str = ''

        for time, day in routines.items():
            routine_str += f'{day} {time}\n'

        formatted_data['routine_id'] = routine_str
        view_data.append(formatted_data)

    student = Student.objects.get(user_id=User.objects.get(username=request.user))
    current_semester = Semester.objects.get(advising_status=True)

    courses_taken = CoursesTaken.objects.filter(
        student_id=student,
        semester_id=current_semester
    ).all()

    view_selected_courses_data = []

    for course in courses_taken:
        formatted_data = {
            'course_code': course.section_id.course_id.course_code,
            'section_no': course.section_id.section_no,
            'section_id': course.section_id.section_id,
            'credits': course.section_id.course_id.credit,
        }

        routines = {}
        for routine in course.section_id.routine_id.timeslot_set.all():
            time_part = str(routine)[2:]
            day_part = str(routine)[0]

            if time_part not in routines:
                routines[time_part] = day_part

            else:
                routines[time_part] += day_part

        routine_str = ''

        for time, day in routines.items():
            routine_str += f'{day} {time}\n'

        formatted_data['routine'] = routine_str
        view_selected_courses_data.append(formatted_data)

    context = {
        'sections': view_data,
        'selected_courses': view_selected_courses_data
    }

    return render(request, 'advising_portal/home.html', context)


@login_required
def add_course(request, section_id):
    current_semester = Semester.objects.get(advising_status=True)
    student = Student.objects.get(user_id=User.objects.get(username=request.user))
    selected_section = Section.objects.get(section_id=section_id)
    selected_course = selected_section.course_id
    selected_routine_slot = selected_section.routine_id

    existence_check = CoursesTaken.objects.filter(
        student_id=student,
        semester_id=current_semester,
        section_id=selected_section
    ).exists()

    if existence_check:
        messages.success(request, 'Section already added')
        return redirect('advising-portal-home')

    elif not existence_check:
        previous_selected_sections = Student.objects.get(
            student_id=student.student_id
        ).coursestaken_set.all()

        courses = []
        routine_slots = []

        for section in previous_selected_sections:
            courses.append(section.section_id.course_id)
            routine_slots.append(section.section_id.routine_id)

        if selected_course in courses:
            messages.success(request, 'Course already added')
            return redirect('advising-portal-home')

        if selected_routine_slot in routine_slots:
            messages.success(request, 'Conflicts')
            return redirect('advising-portal-home')

    if selected_section.total_students < selected_section.section_capacity:
        selected_section.total_students = selected_section.total_students + 1
        selected_section.save()

        course_selected = CoursesTaken(
            student_id=student,
            semester_id=current_semester,
            section_id=selected_section,
        )
        course_selected.save()
        messages.success(request, f'Successfully added Section-{selected_section.section_no} of {selected_section.course_id.course_code}')
    else:
        messages.success(request, 'Section is full!')

    return redirect('advising-portal-home')


@login_required
def drop_course(request, section_id):
    current_semester = Semester.objects.get(advising_status=True)
    student = Student.objects.get(user_id=User.objects.get(username=request.user))
    selected_section = Section.objects.get(section_id=section_id)

    selected_section.total_students = selected_section.total_students - 1
    selected_section.save()

    CoursesTaken.objects.filter(
        student_id=student,
        semester_id=current_semester,
        section_id=selected_section
    ).delete()

    return redirect('advising-portal-home')


@login_required
def view_selected_courses(request):
    student = Student.objects.get(user_id=User.objects.get(username=request.user))
    current_semester = Semester.objects.get(advising_status=True)

    courses_taken = CoursesTaken.objects.filter(
        student_id=student,
        semester_id=current_semester
    ).all()

    view_data = []

    for course in courses_taken:
        formatted_data = {
            'course_code': course.section_id.course_id.course_code,
            'section_no': course.section_id.section_no,
            'section_id': course.section_id.section_id,
            'credits': course.section_id.course_id.credit,
        }

        routines = {}
        for routine in course.section_id.routine_id.timeslot_set.all():
            time_part = str(routine)[2:]
            day_part = str(routine)[0]

            if time_part not in routines:
                routines[time_part] = day_part

            else:
                routines[time_part] += day_part

        routine_str = ''

        for time, day in routines.items():
            routine_str += f'{day} {time}\n'

        formatted_data['routine'] = routine_str
        view_data.append(formatted_data)

    context = {
        'courses': view_data
    }

    return render(request, 'advising_portal/selected_courses.html', context)
