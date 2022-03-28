from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student, RoutineAndTime, TimeSlot, RoutineSlot
from django.contrib.auth.decorators import login_required

import datetime


@login_required
def home(request):
    # sections = list(Section.objects.all())
    student = Student.objects.get(username_id=request.user)

    filter_condition = request.GET.get('filter', 'recommended')

    if filter_condition == 'recommended':
        section_filter = CoursesTaken.objects.filter(
            student_id=student,
            semester_id__in=Semester.objects.filter(
                advising_status=False
            ).values('semester_id').all()
        ).values('section_id').all()

        sections = Section.objects.exclude(
            course_id__in=Section.objects.filter(
                section_id__in=section_filter
            ).values('course_id').all()
        )

        # sections.filter(
        #     course_id__in=Course.objects.filter(
        #         prerequisite_course_id__in=Section.objects.filter(
        #             section_id__in=CoursesTaken.objects.filter(
        #                 student_id=student,
        #                 semester_id__in=Semester.objects.filter(
        #                     advising_status=False
        #                 ).values('semester_id').all()
        #             ).values('section_id').all()
        #         ).values('course_id').all()
        #     ).values('course_id').all()
        # )

    else:
        sections = Section.objects.filter(
            course_id__in=Section.objects.filter(
                section_id__in=CoursesTaken.objects.filter(
                    student_id=student,
                ).values('section_id').all()
            ).values('course_id').all()
        )

        # sections.exclude(
        #     course_id__in=Course.objects.filter(
        #         prerequisite_course_id__in=CoursesTaken.objects.filter(
        #             student_id=student,
        #             semester_id__in=Semester.objects.filter(
        #                 advising_status=False
        #             ).values('semester_id').all()
        #         ).values('section_id')
        #     )
        # )

        # sections.filter(
        #     course_id__in=Course.objects.filter(
        #         prerequisite_course_id__in=Section.objects.filter(
        #             section_id__in=CoursesTaken.objects.filter(
        #                 student_id=student,
        #                 semester_id__in=Semester.objects.filter(
        #                     advising_status=False
        #                 ).values('semester_id').all()
        #             ).values('section_id').all()
        #         ).values('course_id').all()
        #     ).values('course_id').all()
        # )

    sections = list(sections)

    view_data = []

    for section in sections:
        formatted_data = {
            'section_id': section.section_id,
            'section_no': section.section_no,
            'section_capacity': section.section_capacity,
            'total_students': section.total_students,
            'department_name': section.course.department.department_name,
            'instructor_id': section.instructor.name,
            'course_id': section.course.course_code,
            'credit': section.course.credit,
        }

        routines = {}

        get_time_slots = RoutineAndTime.objects.filter(
            routine_slot_id=section.routine_id
        ).values('time_slot_id').distinct()

        for time_slot in get_time_slots:
            time_slot = TimeSlot.objects.get(time_slot_id=time_slot['time_slot_id'])

            time_part = str(time_slot)[2:]
            day_part = str(time_slot)[0]

            if time_part not in routines:
                routines[time_part] = day_part

            else:
                routines[time_part] += day_part

        routine_str = ''

        for time, day in routines.items():
            routine_str += f'{day} {time}\n'

        formatted_data['routine_id'] = routine_str
        view_data.append(formatted_data)

    student_id = Student.objects.get(username_id=request.user).pk
    current_semester_id = Semester.objects.get(advising_status=True).pk

    courses_taken = CoursesTaken.objects.filter(
        student_id=student_id,
        semester_id=current_semester_id
    ).all()

    view_selected_courses_data = []

    for course in courses_taken:
        formatted_data = {
            'course_code': course.section.course.course_code,
            'section_no': course.section.section_no,
            'section_id': course.section_id,
            'credits': course.section.course.credit,
        }

        get_time_slots = RoutineAndTime.objects.filter(
            routine_slot_id=course.section.routine_id
        ).values('time_slot_id').distinct()

        routines = {}

        for routine in get_time_slots:
            time_slot = TimeSlot.objects.get(time_slot_id=routine['time_slot_id'])

            time_part = str(time_slot)[2:]
            day_part = str(time_slot)[0]

            if time_part not in routines:
                routines[time_part] = day_part

            else:
                routines[time_part] += day_part

        routine_str = ''

        for time, day in routines.items():
            routine_str += f'{day} {time} \n'

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
    student = Student.objects.get(username_id=request.user)
    selected_section = Section.objects.get(section_id=section_id)
    selected_course = selected_section.course
    selected_routine_slot = selected_section.routine_id

    selected_routine_slot_chunks = [selected_routine_slot[i:i+3] for i in range(0, len(selected_routine_slot), 3)]

    existence_check = CoursesTaken.objects.filter(
        student=student,
        semester=current_semester,
        section=selected_section
    ).exists()

    if existence_check:
        messages.success(request, 'Section already added')
        return redirect('advising-portal-home')

    elif not existence_check:
        previous_selected_sections = CoursesTaken.objects.filter(
            student_id=student.student_id,
            semester=current_semester,
        ).all()

        for section in previous_selected_sections:
            if section.section.course == selected_course:
                messages.success(request, 'Course already added')
                return redirect('advising-portal-home')

            routine_id = section.section.routine_id

            section_routine_slot_chunks = [routine_id[i:i+3] for i in range(0, len(routine_id), 3)]

            for i in section_routine_slot_chunks:
                for j in selected_routine_slot_chunks:
                    if i == j:
                        messages.success(request, f'Conflicts with {section.section.course.course_code}')
                        # messages.error(request, f'Conflicts with {section.section.course.course_code}')

                        # messages.danger(request, f'Conflicts with {section.section.course.course_code}')
                        return redirect('advising-portal-home')

            # if section.section_id.routine_id == selected_routine_slot:

    if selected_section.total_students < selected_section.section_capacity:
        selected_section.total_students = selected_section.total_students + 1
        selected_section.save()

        course_selected = CoursesTaken(
            student=student,
            semester=current_semester,
            section=selected_section,
        )
        course_selected.save()
        messages.success(request, f'Successfully added Section-{selected_section.section_no} of {selected_section.course.course_code}')
    else:
        messages.success(request, 'Section is full!')

    return redirect('advising-portal-home')


@login_required
def drop_course(request, section_id):
    current_semester_id = Semester.objects.get(advising_status=True).semester_id
    student_id = Student.objects.get(username_id=request.user).student_id
    selected_section = Section.objects.get(section_id=section_id)

    selected_section.total_students = selected_section.total_students - 1
    selected_section.save()

    CoursesTaken.objects.filter(
        student_id=student_id,
        semester_id=current_semester_id,
        section_id=selected_section.section_id
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


@login_required
def view_grade_report(request):
    student = Student.objects.get(username_id=User.objects.get(username=request.user).pk)

    courses_taken = CoursesTaken.objects.filter(
        student_id=student.student_id,
        semester__advising_status=False
    ).all()

    courses_by_semesters = {}

    total_cgpa = 0
    total_credit = 0

    for course in courses_taken:
        total_cgpa += (course.grade.grade_point * course.section.course.credit)
        total_credit += course.section.course.credit

        if course.semester_id not in courses_by_semesters:
            courses_by_semesters[course.semester_id] = {
                'semester_id': course.semester_id,
                'semester_name': course.semester.semester_name,
                'total_credit': course.section.course.credit,
                'courses': [
                    {
                        'course_code': course.section.course.course_code,
                        'course_title': course.section.course.course_title,
                        'course_credit': course.section.course.credit,
                        'grade': course.grade.grade,
                        'total_gp': course.section.course.credit * 4,
                        'grade_point': course.grade.grade_point,
                    }
                ],
                'current_cgpa': total_cgpa,
                'current_total_credit': total_credit,
                'term_gpa': course.grade.grade_point * course.section.course.credit
            }

        else:
            courses_by_semesters[course.semester_id]['total_credit'] += course.section.course.credit
            courses_by_semesters[course.semester_id]['current_cgpa'] = total_cgpa
            courses_by_semesters[course.semester_id]['current_total_credit'] = total_credit
            courses_by_semesters[course.semester_id]['term_gpa'] += (course.grade.grade_point * course.section.course.credit)
            courses_by_semesters[course.semester_id]['courses'].append(
                {
                    'course_code': course.section.course.course_code,
                    'course_title': course.section.course.course_title,
                    'course_credit': course.section.course.credit,
                    'grade': course.grade.grade,
                    'total_gp': course.section.course.credit * 4,
                    'grade_point': course.grade.grade_point,
                }
            )

    for semester in courses_by_semesters.values():
        semester['current_cgpa'] = semester['current_cgpa'] / semester['current_total_credit']
        semester['current_cgpa'] = '{:.2f}'.format(semester['current_cgpa'])

        semester['term_gpa'] = semester['term_gpa'] / semester['total_credit']
        semester['term_gpa'] = '{:.2f}'.format(semester['term_gpa'])

    if total_credit != 0:
        cgpa = total_cgpa / total_credit
        cgpa = '{:.2f}'.format(cgpa)

    else:
        cgpa = 0.0

    context = {
        'cgpa': cgpa,
        'courses_by_semesters': courses_by_semesters
    }

    return render(request, 'advising_portal/grading_report_test.html', context)
