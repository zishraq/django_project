import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from advising_portal.forms import SectionRequestForm
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student, Routine, TimeSlot, WeekSlot, \
    SectionsRequested, Grade
from django.contrib.auth.decorators import login_required

from users.decorators import allowed_users




def get_referer_parameter(request):
    referer = str(request.META.get('HTTP_REFERER'))
    split_referer = referer.split('/')
    referer_parameter = split_referer[-1]

    if not referer_parameter:
        referer_parameter = split_referer[-2]

    return referer_parameter


@login_required
def home(request):
    return render(request, 'advising_portal/student_base.html')


@login_required
@allowed_users(allowed_roles=['student'])
def advising_portal_list_view(request, section_filter):
    student = Student.objects.get(username_id=request.user)

    if section_filter not in ['recommended', 'retakable']:
        section_filter = 'recommended'

    if section_filter == 'recommended':
        ### Get all sections of courses which are not completed
        # get semester ids
        get_semester_ids = Semester.objects.filter(
            advising_status=False
        ).values('semester_id').all()

        # get previous courses
        get_previous_selected_sections = CoursesTaken.objects.filter(
            student_id=student,
            semester_id__in=get_semester_ids
        ).values('section_id').all()

        # exclude previously completed courses
        sections = Section.objects.exclude(
            course_id__in=Section.objects.filter(
                section_id__in=get_previous_selected_sections
            ).values('course_id').all()
        )

        ### exclude courses without pre-requisite completion

        sections = sections.exclude(
            course_id__in=Course.objects.filter(
                prerequisite_course_id__in=Section.objects.exclude(
                    section_id__in=get_previous_selected_sections
                ).values('course_id').all()
            ).values('course_id').all()
        ).order_by('course__course_code')

    else:
        sections = Section.objects.filter(
            course_id__in=Section.objects.filter(
                section_id__in=CoursesTaken.objects.filter(
                    student_id=student,
                    grade_id__in=['C', 'C+', 'C-', 'D', 'D+', 'F']
                ).values('section_id').all()
            ).values('course_id').all()
        ).order_by('course__course_code')

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
            'routine_id': WeekSlot.format_routine(section.routine_id)
        }

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
            'routine_id': WeekSlot.format_routine(course.section.routine_id)
            # 'routine': format_routine(course.section.routine_id)
        }

        view_selected_courses_data.append(formatted_data)

    context = {
        'sections': view_data,
        'selected_courses': view_selected_courses_data,
        'portal_type': 'course_advising'
    }

    return render(request, 'advising_portal/portal.html', context)


@login_required
@allowed_users(allowed_roles=['student'])
def add_course_view(request, section_id):
    referer_parameter = get_referer_parameter(request)

    current_semester = Semester.objects.get(advising_status=True)   # get current semester
    student = Student.objects.get(username_id=request.user)   # get User's student info
    selected_section = Section.objects.get(section_id=section_id)   # get selected section data
    selected_course = selected_section.course   # get course data of the selected section
    selected_routine_slot = selected_section.routine_id   # store routine id of the selected section

    # Split the routine id of the selected section into Time Slots
    selected_routine_slot_chunks = WeekSlot.get_routine_slot_chunks(selected_routine_slot)

    # Check whether the section was already taken
    existence_check = CoursesTaken.objects.filter(
        student=student,
        semester=current_semester,
        section=selected_section
    ).exists()

    if existence_check:
        messages.error(request, 'Section already added')
        return redirect('student-panel-portal', referer_parameter)

    elif not existence_check:
        # Get current selected sections
        previous_selected_sections = CoursesTaken.objects.filter(
            student_id=student.student_id,
            semester=current_semester,
        ).all()

        for section in previous_selected_sections:
            # Check if the course of the section is already taken
            if section.section.course == selected_course:
                messages.error(request, 'Course already added')
                return redirect('student-panel-portal', referer_parameter)

            routine_id = section.section.routine_id   # Get routine id of the comparing section

            # Split the routine id of the comparing section into Time Slots
            section_routine_slot_chunks = WeekSlot.get_routine_slot_chunks(routine_id=routine_id)

            # Check for time slot conflict
            for i in section_routine_slot_chunks:
                for j in selected_routine_slot_chunks:
                    if i == j:
                        messages.error(request, f'Conflicts with {section.section.course.course_code}')
                        return redirect('student-panel-portal', referer_parameter)

            # Check whether total credits exceed limit
            total_credits = Course.objects.filter(
                course_id__in=previous_selected_sections.values('section__course__course_id')
            ).aggregate(Sum('credit'))

            total_credits = total_credits['credit__sum']
            selected_course_credit = selected_course.credit

            if total_credits + selected_course_credit > 12:
                messages.error(request, f'Total credits cannot be more than 12')
                return redirect('student-panel-portal', referer_parameter)

    # check section capacity
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
        messages.error(request, 'Section is full!')

    return redirect('student-panel-portal', referer_parameter)


@login_required
@allowed_users(allowed_roles=['student'])
def drop_course_view(request, section_id):
    referer_parameter = get_referer_parameter(request)

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

    messages.success(request, f'Dropped Section-{selected_section.section_no} of {selected_section.course.course_code}')
    return redirect('student-panel-portal', referer_parameter)


@login_required
@allowed_users(allowed_roles=['student'])
def request_section_list_view(request):
    if request.method == 'POST':
        form = SectionRequestForm(request.POST)

        if form.is_valid():
            reason = form.cleaned_data.get('reason')
            section_id = form.cleaned_data.get('section')

            request_section(request=request, section_id=section_id, reason=reason)

    else:
        form = SectionRequestForm()

    student = Student.objects.get(username_id=request.user)

    sections = Section.objects.exclude(
        section_id__in=CoursesTaken.objects.filter(
            student=student,
            semester_id__in=Semester.objects.filter(
                advising_status=False
            ).values('semester_id').all()
        ).values('section_id').all()
    ).order_by('course__course_code')

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
            'routine_id': WeekSlot.format_routine(section.routine_id)
        }

        view_data.append(formatted_data)

    student_id = Student.objects.get(username_id=request.user).pk
    current_semester_id = Semester.objects.get(advising_status=True).pk

    sections_requested = SectionsRequested.objects.filter(
        student_id=student_id,
        semester_id=current_semester_id
    ).all()

    view_selected_courses_data = []

    for section in sections_requested:
        formatted_data = {
            'course_code': section.section.course.course_code,
            'section_no': section.section.section_no,
            'section_id': section.section_id,
            'credits': section.section.course.credit,
            'routine_id': WeekSlot.format_routine(section.section.routine_id)
        }

        view_selected_courses_data.append(formatted_data)

    context = {
        'sections': view_data,
        'selected_courses': view_selected_courses_data,
        'portal_type': 'section_request',
        'form': form
    }

    return render(request, 'advising_portal/portal.html', context)


def request_section(request, section_id, reason):
    current_semester = Semester.objects.get(advising_status=True)   # get current semester
    student = Student.objects.get(username_id=request.user)   # get User's student info
    requested_section = Section.objects.get(section_id=section_id)   # get selected section data
    selected_course = requested_section.course   # get course data of the selected section
    selected_routine_slot = requested_section.routine_id   # store routine id of the selected section

    # Split the routine id of the selected section into Time Slots
    selected_routine_slot_chunks = [selected_routine_slot[i:i+3] for i in range(0, len(selected_routine_slot), 3)]

    # Check whether the section was already taken
    existence_check = SectionsRequested.objects.filter(
        student=student,
        semester=current_semester,
        section=requested_section
    ).exists()

    if existence_check:
        messages.error(request, 'Already requested for this Section')
        return redirect('student-panel-request-section-list-view')

    elif not existence_check:
        # Get current selected sections
        previous_requested_sections = SectionsRequested.objects.filter(
            student_id=student.student_id,
            semester=current_semester,
        ).all()

        for section in previous_requested_sections:
            # Check if the course of the section is already taken
            if section.section.course == selected_course:
                messages.error(request, 'Already requested for this Course')
                return redirect('student-panel-request-section-list-view')

            routine_id = section.section.routine_id   # Get routine id of the comparing section

            # Split the routine id of the comparing section into Time Slots
            section_routine_slot_chunks = [routine_id[i:i+3] for i in range(0, len(routine_id), 3)]

            # Check for time slot conflict
            for i in section_routine_slot_chunks:
                for j in selected_routine_slot_chunks:
                    if i == j:
                        messages.error(request, f'Conflicts with {section.section.course.course_code}')
                        return redirect('student-panel-request-section-list-view')

            # Check whether total credits exceed limit
            total_credits = Course.objects.filter(
                course_id__in=previous_requested_sections.values('section__course__course_id')
            ).aggregate(Sum('credit'))

            total_credits = total_credits['credit__sum']
            selected_course_credit = selected_course.credit

            credit_limit = 9

            if total_credits + selected_course_credit > credit_limit:
                messages.error(request, f'Cannot request for more than {credit_limit} credits')
                return redirect('student-panel-request-section-list-view')

    # check section capacity
    sections_requested = SectionsRequested(
        student=student,
        semester=current_semester,
        section=requested_section,
        reason=reason
    )
    sections_requested.save()
    messages.success(request, f'Successfully requested for Section-{requested_section.section_no} of {requested_section.course.course_code}')
    return redirect('student-panel-request-section-list-view')


@login_required
@allowed_users(allowed_roles=['student'])
def revoke_section_request_view(request, section_id):
    current_semester_id = Semester.objects.get(advising_status=True).semester_id
    student_id = Student.objects.get(username_id=request.user).student_id
    selected_section = Section.objects.get(section_id=section_id)

    SectionsRequested.objects.filter(
        student_id=student_id,
        semester_id=current_semester_id,
        section_id=selected_section.section_id
    ).delete()

    messages.success(request, f'Request removed for Section-{selected_section.section_no} of {selected_section.course.course_code}')
    return redirect('student-panel-request-section-list-view')


@login_required
@allowed_users(allowed_roles=['student'])
def grade_report_view(request):
    student = Student.objects.get(username_id=User.objects.get(username=request.user).pk)

    courses_taken = CoursesTaken.objects.filter(
        student_id=student.student_id,
        semester__advising_status=False
    ).all()

    courses_by_semesters = {}
    cgpa_progress_list = []
    term_gpa_list = []
    semesters_list = []

    total_cgpa = 0
    total_credit = 0

    grades = list(Grade.objects.all().values('grade').distinct().order_by('-grade_point'))

    grade_frequency = {
        grade['grade']: 0 for grade in grades
    }

    # unique_courses = {
    #     'course_code': {
    #         'total_cgpa'
    #     }
    # }

    for course in courses_taken:
        letter_grade = course.grade.grade
        if letter_grade not in ['D', 'R']:
            course_credit = course.section.course.credit
        else:
            course_credit = 0

        course_code = course.section.course.course_code

        # if course not in unique_courses:
        #     unique_courses[course]

        total_cgpa += (course.grade.grade_point * course_credit)

        total_credit += course_credit

        if course.semester_id not in courses_by_semesters:
            courses_by_semesters[course.semester_id] = {
                'semester_id': course.semester_id,
                'semester_name': course.semester.semester_name,
                'total_credit': course_credit,
                'courses': [
                    {
                        'course_code': course_code,
                        'course_title': re.sub('\(.*\)', '', str(course.section.course.course_title)),
                        'course_credit': course_credit,
                        'grade': letter_grade,
                        'total_gp': course_credit * 4,
                        'grade_point': course.grade.grade_point,
                    }
                ],
                'current_cgpa': total_cgpa,
                'current_total_credit': total_credit,
                'term_gpa': course.grade.grade_point * course_credit
            }

        else:
            courses_by_semesters[course.semester_id]['total_credit'] += course_credit
            courses_by_semesters[course.semester_id]['current_cgpa'] = total_cgpa
            courses_by_semesters[course.semester_id]['current_total_credit'] = total_credit
            courses_by_semesters[course.semester_id]['term_gpa'] += (course.grade.grade_point * course_credit)
            courses_by_semesters[course.semester_id]['courses'].append(
                {
                    'course_code': course_code,
                    'course_title': re.sub('\(.*\)', '', str(course.section.course.course_title)),
                    'course_credit': course_credit,
                    'grade': letter_grade,
                    'total_gp': course_credit * 4,
                    'grade_point': course.grade.grade_point,
                }
            )

    for semester in courses_by_semesters.values():
        semester['current_cgpa'] = semester['current_cgpa'] / semester['current_total_credit']
        semester['current_cgpa'] = round(semester['current_cgpa'], 2)

        semester['term_gpa'] = semester['term_gpa'] / semester['total_credit']
        semester['term_gpa'] = round(semester['term_gpa'], 2)

        cgpa_progress_list.append(semester['current_cgpa'])
        term_gpa_list.append(semester['term_gpa'])
        semesters_list.append(semester['semester_name'])

    for semester in courses_by_semesters.values():
        for course in semester['courses']:
            grade_frequency[course['grade']] += 1

    if total_credit != 0:
        cgpa = total_cgpa / total_credit
        cgpa = round(cgpa, 2)

    else:
        cgpa = 0.0

    context = {
        'cgpa': cgpa,
        'courses_by_semesters': courses_by_semesters,
        'semester_list': semesters_list,
        'cgpa_progress_list': cgpa_progress_list,
        'term_gpa_list': term_gpa_list,
        'grades': list(grade_frequency.keys()),
        'grade_frequency': list(grade_frequency.values()),
        'maximum_grade_frequency': max(list(grade_frequency.values())) + 3
    }

    return render(request, 'advising_portal/grading_report.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def courses_list_view(request):
    courses = Course.objects.all()
    course_list = []

    for course in courses:
        formatted_data = {
            'course_code': course.course_code,
            'course_title': course.course_title,
            'credit': course.credit,
            'department': course.department.department_name,
            'prerequisite_course': course.prerequisite_course.course_code if course.prerequisite_course else '',
        }
        course_list.append(formatted_data)

    context = {
        'courses': course_list
    }

    return render(request, 'advising_portal/courses.html', context)
