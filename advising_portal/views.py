from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student
import datetime


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

    context = {
        'sections': view_data
    }

    return render(request, 'advising_portal/home.html', context)


def select_course(request, section_id):
    # r = CoursesTaken.objects.get(
    #
    # )

    current_semester = Semester.objects.get(advising_status=True)
    # student = Student.objects.get(user_id=request.user)
    student = Student.objects.get(user_id=User.objects.get(username=request.user))
    selected_section = Section.objects.get(section_id=section_id)

    existence_check = CoursesTaken.objects.filter(
        student_id=student,
        semester_id=current_semester,
        section_id=selected_section,
    ).exists()

    if not existence_check:
        messages.success(request, 'Section already taken')

    elif selected_section.total_students < selected_section.section_capacity:
        selected_section.total_students = selected_section.total_students + 1
        selected_section.save()

        course_selected = CoursesTaken(
            student_id=student,
            semester_id=current_semester,
            section_id=selected_section,
        )
        course_selected.save()
        messages.success(request, f'Successfully selected Section-{selected_section.section_no} of {selected_section.course_id.course_code}')
    else:
        messages.success(request, 'Section is full!')

    return redirect('advising-portal-home')
