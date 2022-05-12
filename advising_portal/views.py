import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.utils.encoding import force_str
from django.apps import apps
from django.contrib.admin.models import LogEntry, ADDITION

from advising_portal.forms import SectionRequestForm, CreateCourseForm, CreateSemesterForm, UpdateSectionForm, \
    CreateSectionForm, UpdateSectionRequestForm
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student, Routine, TimeSlot, WeekSlot, \
    SectionsRequested, Grade, Faculty
from django.contrib.auth.decorators import login_required

from advising_portal.utilities import student_id_regex, ADDED, DROPPED, get_referer_parameter, \
    get_conflicting_sections_with_requested_section, text_shorten
from users.decorators import allowed_users


@login_required
def home(request):
    user_id = request.user.id

    context = {
        'room_name': str(user_id)
    }
    return render(request, 'advising_portal/base.html', context)


@login_required
@allowed_users(allowed_roles=['student'])
def advising_portal_list_view(request, section_filter):
    student = Student.objects.get(username_id=request.user)
    user_id = request.user.id

    if section_filter not in ['recommended', 'retakable', 'f', 'd']:
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

    elif section_filter == 'retakable':
        sections = Section.objects.filter(
            course_id__in=Section.objects.filter(
                section_id__in=CoursesTaken.objects.filter(
                    student_id=student,
                    grade_id__in=['C', 'C+', 'C-']
                ).values('section_id').all()
            ).values('course_id').all()
        ).order_by('course__course_code')

    elif section_filter == 'f':
        sections = Section.objects.filter(
            course_id__in=Section.objects.filter(
                section_id__in=CoursesTaken.objects.filter(
                    student_id=student,
                    grade_id__in=['F']
                ).values('section_id').all()
            ).values('course_id').all()
        ).order_by('course__course_code')

    else:
        d_courses = CoursesTaken.objects.filter(
            student_id=student,
            grade_id__in=['D+', 'D']
        ).values('section_id').all()

        get_course_ids = Section.objects.filter(
            section_id__in=d_courses
        ).values('course_id').all()

        sections = Section.objects.filter(
            course_id__in=get_course_ids
        ).order_by('course__course_code')

    sections = list(sections)

    view_section_data = []

    for section in sections:
        formatted_data = {
            'section_id': section.section_id,
            'section_no': section.section_no,
            'section_capacity': section.section_capacity,
            'total_students': section.total_students,
            'department_name': section.course.department.department_name,
            'course_id': section.course.course_code,
            'credit': section.course.credit,
            'routine': section.routine
        }

        view_section_data.append(formatted_data)

    student_id = Student.objects.get(username_id=request.user).pk
    current_semester_id = Semester.objects.get(advising_status=True).pk

    courses_taken = CoursesTaken.objects.filter(
        student_id=student_id,
        semester_id=current_semester_id,
        status=ADDED
    ).all()

    view_selected_courses_data = []

    for course in courses_taken:
        formatted_data = {
            'course_code': course.section.course.course_code,
            'section_no': course.section.section_no,
            'section_id': course.section_id,
            'credits': course.section.course.credit,
            'routine': course.section.routine
        }

        view_selected_courses_data.append(formatted_data)

    context = {
        'sections': view_section_data,
        'selected_courses': view_selected_courses_data,
        'portal_type': 'course_advising',
        'room_name': str(user_id)
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

    # Check whether the section was already taken
    existence_check = CoursesTaken.objects.filter(
        student=student,
        semester=current_semester,
        section=selected_section,
        status=ADDED
    ).exists()

    if existence_check:
        messages.error(request, 'Section already added')
        return redirect('student-panel-portal', referer_parameter)

    elif not existence_check:
        # Get current selected sections
        previous_selected_sections = CoursesTaken.objects.filter(
            student_id=student.student_id,
            semester=current_semester,
            status=ADDED
        ).all()

        for previous_section in previous_selected_sections:
            # Check if the course of the section is already taken
            if previous_section.section.course == selected_course:
                messages.error(request, 'Course already added')
                return redirect('student-panel-portal', referer_parameter)

            if selected_section.does_conflict_with_section(previous_section.section):
                messages.error(request, f'Conflicts with {previous_section.section.course.course_code}')
                return redirect('student-panel-portal', referer_parameter)

            # Check whether total credits exceed limit
            total_credits = Course.objects.filter(
                course_id__in=previous_selected_sections.values('section__course__course_id')
            ).aggregate(Sum('credit'))

            total_credits = total_credits['credit__sum']
            selected_course_credit = selected_course.credit

            credit_limit = 15

            if total_credits + selected_course_credit > credit_limit:
                messages.error(request, f'Total credits cannot be more than {credit_limit}')
                return redirect('student-panel-portal', referer_parameter)

    # check section capacity
    if selected_section.total_students < selected_section.section_capacity:
        selected_section.total_students = selected_section.total_students + 1
        selected_section.save()

        course_selected = CoursesTaken(
            student=student,
            semester=current_semester,
            section=selected_section,
            status=ADDED
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
    current_time = timezone.now()

    current_semester_id = Semester.objects.get(advising_status=True).semester_id
    student_id = Student.objects.get(username_id=request.user).student_id
    selected_section = Section.objects.get(section_id=section_id)

    selected_section.total_students = selected_section.total_students - 1
    selected_section.save()

    drop_course = CoursesTaken.objects.get(
        student_id=student_id,
        semester_id=current_semester_id,
        section_id=selected_section.section_id,
        status=ADDED
    )

    drop_course.dropped_at = current_time
    drop_course.status = DROPPED
    drop_course.updated_by = request.user
    drop_course.save()

    messages.success(request, f'Dropped Section-{selected_section.section_no} of {selected_section.course.course_code}')
    return redirect('student-panel-portal', referer_parameter)


@login_required
@allowed_users(allowed_roles=['student'])
def request_section_list_view(request):
    user_id = request.user.id

    if request.method == 'POST':
        form = SectionRequestForm(request.POST)

        if form.is_valid():
            reason = form.cleaned_data.get('reason')
            section_id = form.cleaned_data.get('section')

            request_section(request=request, section_id=section_id, reason=reason)

    else:
        form = SectionRequestForm()

    current_semester = Semester.objects.get(advising_status=True)   # get current semester
    student = Student.objects.get(username_id=request.user)   # get User's student info

    previous_selected_sections = CoursesTaken.objects.filter(
        student_id=student.student_id,
        semester=current_semester,
        status=ADDED
    ).all()

    sections = Section.objects.exclude(
        section_id__in=CoursesTaken.objects.filter(
            student=student,
            semester_id__in=Semester.objects.filter(
                advising_status=False
            ).values('semester_id').all(),
            status=ADDED
        ).values('section_id').all()
    ).order_by('course__course_code')

    sections = list(sections)

    view_section_data = []

    for section in sections:
        conflicting_sections = get_conflicting_sections_with_requested_section(
            previous_selected_sections=previous_selected_sections,
            selected_section=section
        )

        formatted_data = {
            'section_id': section.section_id,
            'section_no': section.section_no,
            'section_capacity': section.section_capacity,
            'total_students': section.total_students,
            'department_name': section.course.department.department_name,
            'course_id': section.course.course_code,
            'credit': section.course.credit,
            'routine': section.routine,
            'conflicting_sections': conflicting_sections,
        }

        view_section_data.append(formatted_data)

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
            'routine': section.section.routine
        }

        view_selected_courses_data.append(formatted_data)

    context = {
        'sections': view_section_data,
        'selected_courses': view_selected_courses_data,
        'portal_type': 'section_request',
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/portal.html', context)


def request_section(request, section_id, reason):
    current_semester = Semester.objects.get(advising_status=True)   # get current semester
    student = Student.objects.get(username_id=request.user)   # get User's student info
    requested_section = Section.objects.get(section_id=section_id)   # get selected section data
    requested_course = requested_section.course   # get course data of the selected section

    requested_section_routine_id = requested_section.routine_id   # store routine id of the selected section
    time_slots_of_requested_section = Routine.objects.filter(routine_slot_id=requested_section_routine_id)  # get time slots by routine id

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
            semester=current_semester
        ).all()

        for previous_section in previous_requested_sections:
            # Check if the course of the section is already taken
            if previous_section.section.course == requested_course:
                messages.error(request, 'Already requested for this Course')
                return redirect('student-panel-request-section-list-view')

            if requested_section.does_conflict_with_section(previous_section.section):
                messages.error(request, f'Conflicts with {previous_section.section.course.course_code}')
                return redirect('student-panel-request-section-list-view')

            # Check whether total credits exceed limit
            total_credits = Course.objects.filter(
                course_id__in=previous_requested_sections.values('section__course__course_id')
            ).aggregate(Sum('credit'))

            total_credits = total_credits['credit__sum']
            requested_course_credit = requested_course.credit

            credit_limit = 9

            if total_credits + requested_course_credit > credit_limit:
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
    user_id = request.user.id

    courses_taken = CoursesTaken.objects.filter(
        student_id=student.student_id,
        semester__is_active=False,
        status=ADDED
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

    retake_courses = []

    for course in courses_taken:
        letter_grade = course.grade.grade
        grade_point = course.grade.grade_point

        course_code = course.section.course.course_code
        course_credit = course.section.course.credit

        if course_code in retake_courses:
            total_credit += 0
        else:
            total_credit += course_credit

        if letter_grade == 'R':
            retake_courses.append(course_code)

        total_cgpa += (grade_point * course_credit)

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
                        'grade_point': grade_point,
                    }
                ],
                'current_cgpa': total_cgpa,
                'current_total_credit': total_credit,
                'term_gpa': grade_point * course_credit
            }

        else:
            courses_by_semesters[course.semester_id]['total_credit'] += course_credit
            courses_by_semesters[course.semester_id]['current_cgpa'] = total_cgpa
            courses_by_semesters[course.semester_id]['current_total_credit'] = total_credit
            courses_by_semesters[course.semester_id]['term_gpa'] += (grade_point * course_credit)
            courses_by_semesters[course.semester_id]['courses'].append(
                {
                    'course_code': course_code,
                    'course_title': re.sub('\(.*\)', '', str(course.section.course.course_title)),
                    'course_credit': course_credit,
                    'grade': letter_grade,
                    'total_gp': course_credit * 4,
                    'grade_point': grade_point,
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
        'maximum_grade_frequency': max(list(grade_frequency.values())) + 3,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/grading_report.html', context)


@login_required
@allowed_users(allowed_roles=['student'])
def advised_course_list_view(request):
    user_id = request.user.id
    student_id = Student.objects.get(username_id=request.user).pk
    semester_id = request.GET.get('semester_id', '')

    if not semester_id:
        semester_id = Semester.objects.get(advising_status=True).pk

    semester = Semester.objects.get(semester_id=semester_id)

    semesters = list(Semester.objects.all().order_by('-semester_id'))

    courses_taken = CoursesTaken.objects.filter(
        student_id=student_id,
        semester_id=semester.semester_id,
        status=ADDED
    ).all()

    view_selected_courses_data = []

    for course in courses_taken:
        formatted_data = {
            'course_code': course.section.course.course_code,
            'section_no': course.section.section_no,
            'section_id': course.section_id,
            'credits': course.section.course.credit,
            'routine': course.section.routine
        }

        view_selected_courses_data.append(formatted_data)

    context = {
        'selected_courses': view_selected_courses_data,
        'portal_type': 'course_advising',
        'semesters': semesters,
        'is_advising_semester': semester.advising_status,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/advised_course_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_list_view(request):
    courses = Course.objects.all()
    user_id = request.user.id
    course_list = []

    for course in courses:
        formatted_data = {
            'course_id': course.course_id,
            'course_code': course.course_code,
            'course_title': course.course_title,
            'credit': course.credit,
            'department': course.department.department_name,
            'prerequisite_course': course.prerequisite_course.course_code if course.prerequisite_course else '',
        }
        course_list.append(formatted_data)

    context = {
        'courses': course_list,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/course_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_detail_view(request, course_id):
    user_id = request.user.id

    course_data = Course.objects.get(
        course_id=course_id
    )

    if request.method == 'POST':
        form = CreateCourseForm(request.POST, instance=course_data)

        if form.is_valid():
            form.save()

            messages.success(request, 'Course successfully updated!')
            return redirect('student-panel-course-detail', course_id)

    else:
        form = CreateCourseForm(instance=course_data)

    sections = Section.objects.filter(course_id=course_id)
    section_list = []

    for section in sections:
        if section.instructor:
            instructor_initials = section.instructor.initials
            instructor_name = section.instructor.name
        else:
            instructor_initials = ''
            instructor_name = ''

        formatted_data = {
            'section_id': section.section_id,
            'section_no': section.section_no,
            'section_capacity': section.section_capacity,
            'total_students': section.total_students,
            'instructor_initials': instructor_initials,
            'instructor_name': instructor_name,
            'formatted_routine': section.routine
        }

        section_list.append(formatted_data)

    HistoricalCourse = apps.get_model('advising_portal', 'HistoricalCourse')

    course_history = HistoricalCourse.objects.all()

    context = {
        'form': form,
        'sections': section_list,
        'course_code': course_data.course_code,
        'course_id': course_data.course_id,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/course_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_create_view(request):
    user_id = request.user.id

    if request.method == 'POST':
        form = CreateCourseForm(request.POST)

        if form.is_valid():
            create_course_data = form.cleaned_data
            create_course_data['course_id'] = create_course_data['course_code']

            new_course = Course(**create_course_data)
            new_course.save()

            messages.success(request, 'Course successfully created!')
            return redirect('student-panel-course-list')

    else:
        form = CreateCourseForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/create_course.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_delete_view(request, course_id):
    course_data = Course.objects.get(course_id=course_id)

    Course.objects.filter(
        course_id=course_id
    ).delete()

    messages.success(request, f'Deleted course {course_data.course_code}')
    return redirect('student-panel-course-list')


@login_required
@allowed_users(allowed_roles=['faculty'])
def section_detail_view(request, section_id):
    user_id = request.user.id

    section_data = Section.objects.get(
        section_id=section_id
    )

    if request.method == 'POST':
        form = UpdateSectionForm(request.POST, instance=section_data)

        if form.is_valid():
            instructor = form.cleaned_data['instructor']

            instructors_sections = Section.objects.filter(
                instructor=instructor
            )

            for section in instructors_sections:
                if section_data.does_conflict_with_section(section):
                    messages.error(request, f'Instructor assigned to Section-{section.section_no} of Course {section.course.course_code}!')
                    return redirect('student-panel-section-detail', section_id)

            form.save()

            messages.success(request, 'Section successfully updated!')
            return redirect('student-panel-course-detail', section_data.course_id)

    else:
        form = UpdateSectionForm(instance=section_data)

    context = {
        'form': form,
        'course_code': section_data.course.course_code,
        'section_no': section_data.section_no,
        'section_id': section_data.section_id,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def section_create_view(request, course_code):
    user_id = request.user.id

    if request.method == 'POST':
        form = CreateSectionForm(request.POST)

        if form.is_valid():
            course_data = Course.objects.get(
                course_code=course_code
            )

            create_section_data = form.cleaned_data
            create_section_data['section_id'] = course_code + str(create_section_data['section_no'])
            create_section_data['course'] = course_data
            create_section_data['created_at'] = timezone.now()
            create_section_data['created_by'] = request.user

            new_section = Section(**create_section_data)
            new_section.save()

            messages.success(request, 'Section successfully added!')
            return redirect('student-panel-course-detail', course_code)

    else:
        form = CreateSectionForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_create.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def section_delete_view(request, section_id):
    section_data = Section.objects.get(section_id=section_id)

    Section.objects.filter(
        section_id=section_id
    ).delete()

    messages.success(request, f'Deleted section-{section_data.section_no} of course {section_data.course.course_code}')
    return redirect('student-panel-course-detail', section_data.course.course_code)


@login_required
@allowed_users(allowed_roles=['faculty'])
def semester_list_view(request):
    user_id = request.user.id
    semesters = Semester.objects.all().order_by('-semester_id')
    semester_list = []

    for semester in semesters:
        formatted_data = {
            'semester_id': semester.semester_id,
            'semester_name': semester.semester_name,
            'semester_starts_at': semester.semester_starts_at,
            'semester_ends_at': semester.semester_ends_at,
            'advising_status': 'Yes' if semester.advising_status else 'No',
            'add_drop_status': 'Yes' if semester.add_drop_status else 'No',
            'is_active': 'Yes' if semester.is_active else 'No'
        }
        semester_list.append(formatted_data)

    context = {
        'semesters': semester_list,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/semester_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def semester_detail_view(request, semester_id):
    user_id = request.user.id

    semester_data = Semester.objects.get(
        semester_id=semester_id
    )

    if request.method == 'POST':
        form = CreateSemesterForm(request.POST, instance=semester_data)

        if form.is_valid():
            update_semester_data = form.cleaned_data
            update_semester_data['updated_at'] = timezone.now()
            update_semester_data['updated_by'] = request.user

            updated_semester = Semester(**update_semester_data)
            updated_semester.save()

            messages.success(request, 'Semester successfully updated!')
            return redirect('student-panel-semester-list')

    else:
        form = CreateSemesterForm(instance=semester_data)

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/semester_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def semester_create(request):
    user_id = request.user.id

    if request.method == 'POST':
        form = CreateSemesterForm(request.POST)

        if form.is_valid():
            create_semester_data = form.cleaned_data
            create_semester_data['created_at'] = timezone.now()
            create_semester_data['created_by'] = request.user

            new_semester = Semester(**create_semester_data)
            new_semester.save()

            messages.success(request, 'Semester successfully created!')
            return redirect('student-panel-semester-list')

    else:
        form = CreateSemesterForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/create_semester.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def assigned_sections(request):
    user_id = request.user.id
    get_faculty = Faculty.objects.get(username=request.user)

    instructors_sections = Section.objects.filter(
        instructor=get_faculty
    )

    view_section_data = []

    for section in instructors_sections:
        formatted_data = {
            'section_id': section.section_id,
            'section_no': section.section_no,
            'section_capacity': section.section_capacity,
            'total_students': section.total_students,
            'department_name': section.course.department.department_name,
            'course_code': section.course.course_code,
            'credit': section.course.credit,
            'routine': section.routine
        }

        view_section_data.append(formatted_data)

    context = {
        'sections': view_section_data,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/assigned_section_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def section_request_list_view(request):
    user_id = request.user.id
    user = request.user

    # section_requests = SectionsRequested.objects.all()
    #
    # section_requests = SectionsRequested.objects.filter(
    #     student__advisor__username=user,
    #     # student__advisor__username_id=user_id,
    #     # section__instructor__username_id=user_id
    #     section__instructor__username=user
    # )

    section_requests = SectionsRequested.objects.filter(
        Q(student__advisor__username_id=user_id) | Q(section__instructor__username=user_id)
    )

    section_requests_list = []

    for section_request in section_requests:
        print(user_id)
        print(section_request.student.advisor.username.id)
        # print(section_request['student__advisor__username_id'])
        # print(section_request['section__instructor__username_id'])

        formatted_data = {
            'request_id': section_request.request_id,
            'student_id': section_request.student.student_id,
            'student_name': section_request.student.name,
            'course_code': section_request.section.course.course_code,
            'section_no': section_request.section.section_no,
            'reason': text_shorten(text=section_request.reason, length=100),
            'is_approved_by_advisor': section_request.advisor_approval_status,
            'is_approved_by_chairman': section_request.chairman_approval_status,
            'is_approved_by_instructor': section_request.instructor_approval_status
        }
        section_requests_list.append(formatted_data)

    context = {
        'section_requests': section_requests_list,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_request_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def section_request_detail_view(request, request_id):
    user_id = request.user.id
    user = request.user

    section_request_data = SectionsRequested.objects.get(
        request_id=request_id
    )

    is_faculty = False
    is_advisor = False
    is_chairman = False

    current_faculty_data = Faculty.objects.get(
        username__id=user_id
    )

    student_advisor = section_request_data.student.advisor.username
    section_instructor = section_request_data.section.instructor.username
    department_chairman = section_request_data.section.course.department.chairman

    if request.method == 'POST':
        form = UpdateSectionRequestForm(request.POST)

        if form.is_valid():
            update_semester_data = form.cleaned_data

            if current_faculty_data == student_advisor:
                section_request_data.advisor = current_faculty_data
                section_request_data.advisor_approval_status = update_semester_data['is_approved']
                section_request_data.advisor_text = update_semester_data['text']

            if current_faculty_data == section_instructor:
                section_request_data.instructor = current_faculty_data
                section_request_data.instructor_approval_status = update_semester_data['is_approved']
                section_request_data.instructor_text = update_semester_data['text']

            if current_faculty_data == department_chairman:
                section_request_data.chairman = current_faculty_data
                section_request_data.chairman_approval_status = update_semester_data['is_approved']
                section_request_data.chairman_text = update_semester_data['text']

            # if section_request_data.advisor_approval_status == section_request_data.instructor_approval_status == section_request_data.chairman_approval_status == 'approved':


            section_request_data.save()

            messages.success(request, 'Semester successfully updated!')
            return redirect('student-panel-section-request-list')

    else:
        form = UpdateSectionRequestForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_request_detail.html', context)


def insert_test_data(request):
    from advising_portal.models import WeekSlot, TimeSlot, Routine, Department, Course, Faculty, Section, Student, Semester, Grade, CoursesTaken
    from django.contrib.auth.models import User, Group
    import datetime
    from django.utils import timezone

    groups = [
        {
            'name': 'student',
        },
        {
            'name': 'faculty',
        },
        {
            'name': 'chairman',
        }
    ]

    for g in groups:
        group = Group.objects.create(**g)
        group.save()

    users = [
        {
            'username': 'admin',
            'password': 'admin',
            'is_superuser': True,
            'is_staff': True
        },
        {
            'username': '2020-1-65-001',
            'password': '123456Seven'
        },
        {
            'username': '2019-2-60-015',
            'password': '123456Seven'
        },
        {
            'username': '2019-2-60-022',
            'password': '123456Seven'
        },
        {
            'username': '2019-2-60-025',
            'password': '123456Seven'
        },
        {
            'username': '2018-2-60-127',
            'password': '123456Seven'
        },
        {
            'username': '2020-1-60-226',
            'password': '123456Seven'
        },
        {
            'username': 'ishraq',
            'password': '123456Seven'
        },
        {
            'username': 'nusrat',
            'password': '123456Seven'
        },
        {
            'username': 'tanvir',
            'password': '123456Seven'
        },
        {
            'username': 'rajib',
            'password': '123456Seven'
        },
        {
            'username': 'sadat',
            'password': '123456Seven'
        }
    ]

    for u in users:
        user = User.objects.create_user(**u)
        user.save()

        if re.match(student_id_regex, user.username):
            group = Group.objects.get(name='student')
            group.user_set.add(user)

        else:
            group = Group.objects.get(name='faculty')
            group.user_set.add(user)

    departments = [
        {
            'department_id': 'CSE',
            'department_name': 'Computer Science and Engineering',
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'chairman_id': User.objects.get(username='nusrat').pk
        },
        {
            'department_id': 'GEN',
            'department_name': 'General',
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'chairman_id': User.objects.get(username='tanvir').pk
        }
    ]

    for i in departments:
        r = Department(**i)
        r.save()

    semesters = [
        {
            'semester_id': 1,
            'semester_name': 'Summer-2018',
            'semester_starts_at': datetime.datetime(year=2018, month=5, day=4),
            'semester_ends_at': datetime.datetime(year=2018, month=8, day=18),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 2,
            'semester_name': 'Fall-2018',
            'semester_starts_at': datetime.datetime(year=2018, month=9, day=1),
            'semester_ends_at': datetime.datetime(year=2018, month=12, day=17),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 3,
            'semester_name': 'Spring-2019',
            'semester_starts_at': datetime.datetime(year=2019, month=1, day=3),
            'semester_ends_at': datetime.datetime(year=2019, month=4, day=20),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 4,
            'semester_name': 'Summer-2019',
            'semester_starts_at': datetime.datetime(year=2019, month=5, day=4),
            'semester_ends_at': datetime.datetime(year=2019, month=8, day=18),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 5,
            'semester_name': 'Fall-2019',
            'semester_starts_at': datetime.datetime(year=2019, month=9, day=1),
            'semester_ends_at': datetime.datetime(year=2019, month=12, day=17),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 6,
            'semester_name': 'Spring-2020',
            'semester_starts_at': datetime.datetime(year=2020, month=1, day=3),
            'semester_ends_at': datetime.datetime(year=2020, month=4, day=20),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 7,
            'semester_name': 'Summer-2020',
            'semester_starts_at': datetime.datetime(year=2020, month=5, day=7),
            'semester_ends_at': datetime.datetime(year=2020, month=8, day=15),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 8,
            'semester_name': 'Fall-2020',
            'semester_starts_at': datetime.datetime(year=2020, month=9, day=6),
            'semester_ends_at': datetime.datetime(year=2020, month=12, day=17),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 9,
            'semester_name': 'Spring-2021',
            'semester_starts_at': datetime.datetime(year=2021, month=1, day=9),
            'semester_ends_at': datetime.datetime(year=2021, month=4, day=19),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 10,
            'semester_name': 'Summer-2021',
            'semester_starts_at': datetime.datetime(year=2021, month=5, day=12),
            'semester_ends_at': datetime.datetime(year=2021, month=8, day=24),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 11,
            'semester_name': 'Fall-2021',
            'semester_starts_at': datetime.datetime(year=2021, month=9, day=9),
            'semester_ends_at': datetime.datetime(year=2021, month=12, day=19),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': False
        },
        {
            'semester_id': 12,
            'semester_name': 'Spring-2022',
            'semester_starts_at': datetime.datetime(year=2022, month=2, day=6),
            'semester_ends_at': datetime.datetime(year=2022, month=5, day=18),
            'created_at': timezone.now(),
            'created_by_id': User.objects.get(username='admin').pk,
            'advising_status': True,
            'is_active': True
        }
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
            'course_id': 'MAT101',
            'course_code': 'MAT101',
            'course_title': 'Differential and Integral Calculus',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 3,
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
            'course_id': 'MAT102',
            'course_code': 'MAT102',
            'course_title': 'Differential Equations and Special Functions',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': 'MAT101',
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
            'course_id': 'MAT104',
            'course_code': 'MAT104',
            'course_title': 'Co-ordinate Geometry & Vector Analysis',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "MAT101",
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CHE109',
            'course_code': 'CHE109',
            'course_title': 'Engineering Chemistry-I',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE209',
            'course_code': 'CSE209',
            'course_title': 'Electrical Circuits',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': None,
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'MAT205',
            'course_code': 'MAT205',
            'course_title': 'Linear Algebra & Complex Variables',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "MAT102",
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
            'course_title': 'Principles of Microeconomics',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'CSE251',
            'course_code': 'CSE251',
            'course_title': 'Electronic Circuits',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': 'CSE209',
            'credit': 4,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'STA102',
            'course_code': 'STA102',
            'course_title': 'Statistics and Probability',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': None,
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        },
        {
            'course_id': 'PHY109',
            'course_code': 'PHY109',
            'course_title': 'Engineering Physics-I (Introductory Classical Physics)',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': 'MAT205',
            'credit': 4,
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
            'course_id': 'BUS231',
            'course_code': 'BUS231',
            'course_title': 'Engineering Physics-I (Introductory Classical Physics)',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': 'MAT205',
            'credit': 3,
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
            'course_id': 'CSE246',
            'course_code': 'CSE246',
            'course_title': 'Algorithms',
            'department_id': Department.objects.get(pk='CSE').pk,
            'prerequisite_course_id': 'CSE207',
            'credit': 4.5,
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
            'prerequisite_course_id': "CSE251",
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
            'course_id': 'PHY209',
            'course_code': 'PHY209',
            'course_title': 'Engineering Physics-II (Introductory Quantum Physics)',
            'department_id': Department.objects.get(pk='GEN').pk,
            'prerequisite_course_id': "PHY109",
            'credit': 3,
            'created_by_id': User.objects.get(username='admin').pk
        }
    ]

    for i in courses:
        r = Course(**i)
        r.save()

    faculties = [
        {
            'faculty_id': 'ZI',
            'name': 'Zuhair Ishraq',
            'initials': 'ZI',
            'gender': 'male',
            'username_id': User.objects.get(username='ishraq').pk
        },
        {
            'faculty_id': 'NM',
            'name': 'Nusrat Maisha',
            'initials': 'NM',
            'gender': 'male',
            'username_id': User.objects.get(username='nusrat').pk
        },
        {
            'faculty_id': 'TM',
            'name': 'Tanvir Mobasshir',
            'initials': 'TM',
            'gender': 'male',
            'username_id': User.objects.get(username='tanvir').pk
        },
        {
            'faculty_id': 'RR',
            'name': 'Rajib Raiyat',
            'initials': 'RR',
            'gender': 'male',
            'username_id': User.objects.get(username='rajib').pk
        },
        {
            'faculty_id': 'AKMS',
            'name': 'AKM Sadat',
            'initials': 'AKMS',
            'gender': 'male',
            'username_id': User.objects.get(username='sadat').pk
        },
        {
            'faculty_id': 'admin',
            'name': 'admin',
            'initials': 'admin',
            'gender': 'male',
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
            'start_time': datetime.time(hour=8, minute=30, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'S02': {
            'time_slot_id': 'S02',
            'day': 'S',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=11, minute=40, second=0)
        },
        'S03': {
            'time_slot_id': 'S03',
            'day': 'S',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=13, minute=20, second=0)
        },
        'S04': {
            'time_slot_id': 'S04',
            'day': 'S',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=0, second=0)
        },
        'S05': {
            'time_slot_id': 'S05',
            'day': 'S',
            'start_time': datetime.time(hour=15, minute=10, second=0),
            'end_time': datetime.time(hour=16, minute=40, second=0)
        },
        'S06': {
            'time_slot_id': 'S06',
            'day': 'S',
            'start_time': datetime.time(hour=8, minute=00, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'S07': {
            'time_slot_id': 'S07',
            'day': 'S',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=12, minute=10, second=0)
        },
        'S08': {
            'time_slot_id': 'S08',
            'day': 'S',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=30, second=0)
        },
        'S09': {
            'time_slot_id': 'S09',
            'day': 'S',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=18, minute=50, second=0)
        },
        'S10': {
            'time_slot_id': 'S10',
            'day': 'S',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=14, minute=50, second=0)
        },
        'S11': {
            'time_slot_id': 'S11',
            'day': 'S',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=19, minute=50, second=0)
        },
        'M01': {
            'time_slot_id': 'M01',
            'day': 'M',
            'start_time': datetime.time(hour=8, minute=30, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'M02': {
            'time_slot_id': 'M02',
            'day': 'M',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=11, minute=40, second=0)
        },
        'M03': {
            'time_slot_id': 'M03',
            'day': 'M',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=13, minute=20, second=0)
        },
        'M04': {
            'time_slot_id': 'M04',
            'day': 'M',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=0, second=0)
        },
        'M05': {
            'time_slot_id': 'M05',
            'day': 'M',
            'start_time': datetime.time(hour=15, minute=10, second=0),
            'end_time': datetime.time(hour=16, minute=40, second=0)
        },
        'M06': {
            'time_slot_id': 'M06',
            'day': 'M',
            'start_time': datetime.time(hour=8, minute=00, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'M07': {
            'time_slot_id': 'M07',
            'day': 'M',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=12, minute=10, second=0)
        },
        'M08': {
            'time_slot_id': 'M08',
            'day': 'M',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=30, second=0)
        },
        'M09': {
            'time_slot_id': 'M09',
            'day': 'M',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=18, minute=50, second=0)
        },
        'M10': {
            'time_slot_id': 'M10',
            'day': 'M',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=14, minute=50, second=0)
        },
        'M11': {
            'time_slot_id': 'M11',
            'day': 'M',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=19, minute=50, second=0)
        },
        'T01': {
            'time_slot_id': 'T01',
            'day': 'T',
            'start_time': datetime.time(hour=8, minute=30, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'T02': {
            'time_slot_id': 'T02',
            'day': 'T',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=11, minute=40, second=0)
        },
        'T03': {
            'time_slot_id': 'T03',
            'day': 'T',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=13, minute=20, second=0)
        },
        'T04': {
            'time_slot_id': 'T04',
            'day': 'T',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=0, second=0)
        },
        'T05': {
            'time_slot_id': 'T05',
            'day': 'T',
            'start_time': datetime.time(hour=15, minute=10, second=0),
            'end_time': datetime.time(hour=16, minute=40, second=0)
        },
        'T06': {
            'time_slot_id': 'T06',
            'day': 'T',
            'start_time': datetime.time(hour=8, minute=00, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'T07': {
            'time_slot_id': 'T07',
            'day': 'T',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=12, minute=10, second=0)
        },
        'T08': {
            'time_slot_id': 'T08',
            'day': 'T',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=30, second=0)
        },
        'T09': {
            'time_slot_id': 'T09',
            'day': 'T',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=18, minute=50, second=0)
        },
        'T10': {
            'time_slot_id': 'T10',
            'day': 'T',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=14, minute=50, second=0)
        },
        'T11': {
            'time_slot_id': 'T11',
            'day': 'T',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=19, minute=50, second=0)
        },
        'W01': {
            'time_slot_id': 'W01',
            'day': 'W',
            'start_time': datetime.time(hour=8, minute=30, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'W02': {
            'time_slot_id': 'W02',
            'day': 'W',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=11, minute=40, second=0)
        },
        'W03': {
            'time_slot_id': 'W03',
            'day': 'W',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=13, minute=20, second=0)
        },
        'W04': {
            'time_slot_id': 'W04',
            'day': 'W',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=0, second=0)
        },
        'W05': {
            'time_slot_id': 'W05',
            'day': 'W',
            'start_time': datetime.time(hour=15, minute=10, second=0),
            'end_time': datetime.time(hour=16, minute=40, second=0)
        },
        'W06': {
            'time_slot_id': 'W06',
            'day': 'W',
            'start_time': datetime.time(hour=8, minute=00, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'W07': {
            'time_slot_id': 'W07',
            'day': 'W',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=12, minute=10, second=0)
        },
        'W08': {
            'time_slot_id': 'W08',
            'day': 'W',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=30, second=0)
        },
        'W09': {
            'time_slot_id': 'W09',
            'day': 'W',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=18, minute=50, second=0)
        },
        'W10': {
            'time_slot_id': 'W10',
            'day': 'W',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=14, minute=50, second=0)
        },
        'W11': {
            'time_slot_id': 'W11',
            'day': 'W',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=19, minute=50, second=0)
        },
        'R01': {
            'time_slot_id': 'R01',
            'day': 'R',
            'start_time': datetime.time(hour=8, minute=30, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'R02': {
            'time_slot_id': 'R02',
            'day': 'R',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=11, minute=40, second=0)
        },
        'R03': {
            'time_slot_id': 'R03',
            'day': 'R',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=13, minute=20, second=0)
        },
        'R04': {
            'time_slot_id': 'R04',
            'day': 'R',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=0, second=0)
        },
        'R05': {
            'time_slot_id': 'R05',
            'day': 'R',
            'start_time': datetime.time(hour=15, minute=10, second=0),
            'end_time': datetime.time(hour=16, minute=40, second=0)
        },
        'R06': {
            'time_slot_id': 'R06',
            'day': 'R',
            'start_time': datetime.time(hour=8, minute=00, second=0),
            'end_time': datetime.time(hour=10, minute=0, second=0)
        },
        'R07': {
            'time_slot_id': 'R07',
            'day': 'R',
            'start_time': datetime.time(hour=10, minute=10, second=0),
            'end_time': datetime.time(hour=12, minute=10, second=0)
        },
        'R08': {
            'time_slot_id': 'R08',
            'day': 'R',
            'start_time': datetime.time(hour=13, minute=30, second=0),
            'end_time': datetime.time(hour=15, minute=30, second=0)
        },
        'R09': {
            'time_slot_id': 'R09',
            'day': 'R',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=18, minute=50, second=0)
        },
        'R10': {
            'time_slot_id': 'R10',
            'day': 'R',
            'start_time': datetime.time(hour=11, minute=50, second=0),
            'end_time': datetime.time(hour=14, minute=50, second=0)
        },
        'R11': {
            'time_slot_id': 'R11',
            'day': 'R',
            'start_time': datetime.time(hour=16, minute=50, second=0),
            'end_time': datetime.time(hour=19, minute=50, second=0)
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
            'routine_id': 'S01T01R01'
        },
        {
            'routine_id': 'S01T01R06'
        },
        {
            'routine_id': 'S01T01R09'
        },
        {
            'routine_id': 'S01T01R11'
        },
        {
            'routine_id': 'S03T03R06'
        },
        {
            'routine_id': 'S03T03R09'
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
            'routine_id': 'S01R01T06'
        },
        {
            'routine_id': 'S01R01T09'
        },
        {
            'routine_id': 'S01R01R09'
        },
        {
            'routine_id': 'S01R01T11'
        },
        {
            'routine_id': 'S03R03T06'
        },
        {
            'routine_id': 'S03R03T09'
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
            'routine_id': 'T01R01R11'
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
            'routine_id': 'M01W01W07'
        },
        {
            'routine_id': 'M01W01W09'
        },
        {
            'routine_id': 'M01W01W11'
        },
        {
            'routine_id': 'M03W03W09'
        },
        {
            'routine_id': 'T01'
        }
    ]

    c = 1

    for i in routine_slot:
        r = WeekSlot(**i)
        r.save()

        routine_id = i['routine_id']
        selected_routine_slot_chunks = [routine_id[i:i + 3] for i in range(0, len(routine_id), 3)]

        for chunk in selected_routine_slot_chunks:
            routine_data = {
                'routine_slot_id': routine_id,
                'time_slot_id': chunk
            }

            rt = Routine(**routine_data)
            rt.save()

    sections = [
        {
            'section_id': 'CSE1031',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W11').pk,
            'course_id': Course.objects.get(pk='CSE103').pk,
        },
        {
            'section_id': 'ENG1011',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03T03').pk,
            'course_id': Course.objects.get(pk='ENG101').pk,
        },
        {
            'section_id': 'CSE1061',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01T01').pk,
            'course_id': Course.objects.get(pk='CSE106').pk,
        },
        {
            'section_id': 'ENG1021',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03T03').pk,
            'course_id': Course.objects.get(pk='ENG102').pk,
        },
        {
            'section_id': 'MAT1011',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S04T04').pk,
            'course_id': Course.objects.get(pk='MAT101').pk,
        },
        {
            'section_id': 'CSE1062',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S04T04').pk,
            'course_id': Course.objects.get(pk='CSE106').pk,
        },
        {
            'section_id': 'MAT1021',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S04T04').pk,
            'course_id': Course.objects.get(pk='MAT102').pk,
        },
        {
            'section_id': 'CSE1101',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01R01T11').pk,
            'course_id': Course.objects.get(pk='CSE110').pk,
        },
        {
            'section_id': 'MAT1041',
            'section_no': 1,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01').pk,
            'course_id': Course.objects.get(pk='MAT104').pk,
        },
        {
            'section_id': 'CHE1091',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W07').pk,
            'course_id': Course.objects.get(pk='CHE109').pk,
        },
        {
            'section_id': 'CSE2091',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03R03T06').pk,
            'course_id': Course.objects.get(pk='CSE209').pk,
        },
        {
            'section_id': 'CSE2511',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01T01R01').pk,
            'course_id': Course.objects.get(pk='CSE251').pk,
        },
        {
            'section_id': 'CSE2001',
            'section_no': 1,
            'section_capacity': 40,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='T01').pk,
            'course_id': Course.objects.get(pk='CSE200').pk,
        },
        {
            'section_id': 'MAT2051',
            'section_no': 1,
            'section_capacity': 40,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03T03').pk,
            'course_id': Course.objects.get(pk='MAT205').pk,
        },
        {
            'section_id': 'GEN2261',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='T03R03').pk,
            'course_id': Course.objects.get(pk='GEN226').pk,
        },
        {
            'section_id': 'ECO1011',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S05R05').pk,
            'course_id': Course.objects.get(pk='ECO101').pk,
        },
        {
            'section_id': 'CSE2461',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W09').pk,
            'course_id': Course.objects.get(pk='CSE246').pk,
        },
        {
            'section_id': 'CSE2071',
            'section_no': 1,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W11').pk,
            'course_id': Course.objects.get(pk='CSE207').pk,
        },
        {
            'section_id': 'CSE4051',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03T03R06').pk,
            'course_id': Course.objects.get(pk='CSE405').pk,
        },
        {
            'section_id': 'CSE4052',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W09').pk,
            'course_id': Course.objects.get(pk='CSE405').pk,
        },
        {
            'section_id': 'CSE3021',
            'section_no': 1,
            'section_capacity': 40,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01T01R11').pk,
            'course_id': Course.objects.get(pk='CSE302').pk,
        },
        {
            'section_id': 'CSE3251',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W07').pk,
            'course_id': Course.objects.get(pk='CSE325').pk,
        },
        {
            'section_id': 'CSE3451',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01R01T09').pk,
            'course_id': Course.objects.get(pk='CSE345').pk,
        },
        {
            'section_id': 'STA1021',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M05W05').pk,
            'course_id': Course.objects.get(pk='STA102').pk,
        },
        {
            'section_id': 'CSE3471',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03T03R09').pk,
            'course_id': Course.objects.get(pk='CSE347').pk,
        },
        {
            'section_id': 'CSE3472',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M03W03W09').pk,
            'course_id': Course.objects.get(pk='CSE347').pk,
        },
        {
            'section_id': 'CSE3601',
            'section_no': 1,
            'section_capacity': 45,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01').pk,
            'course_id': Course.objects.get(pk='CSE360').pk,
        },
        {
            'section_id': 'ENG1012',
            'section_no': 2,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='T05R05').pk,
            'course_id': Course.objects.get(pk='ENG101').pk,
        },
        {
            'section_id': 'ENG1022',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S05R05').pk,
            'course_id': Course.objects.get(pk='ENG102').pk,
        },
        {
            'section_id': 'GEN2031',
            'section_no': 1,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S05T05').pk,
            'course_id': Course.objects.get(pk='GEN203').pk,
        },
        {
            'section_id': 'GEN2032',
            'section_no': 2,
            'section_capacity': 35,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M05W05').pk,
            'course_id': Course.objects.get(pk='GEN203').pk,
        },
        {
            'section_id': 'GEN2141',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01').pk,
            'course_id': Course.objects.get(pk='GEN214').pk,
        },
        {
            'section_id': 'GEN2142',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01R01').pk,
            'course_id': Course.objects.get(pk='GEN214').pk,
        },
        {
            'section_id': 'GEN2101',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S03T03').pk,
            'course_id': Course.objects.get(pk='GEN210').pk,
        },
        {
            'section_id': 'GEN2102',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S04T04').pk,
            'course_id': Course.objects.get(pk='GEN210').pk,
        },
        {
            'section_id': 'BUS2311',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S02T02').pk,
            'course_id': Course.objects.get(pk='BUS231').pk,
        },
        {
            'section_id': 'PHY1091',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='M01W01W07').pk,
            'course_id': Course.objects.get(pk='PHY109').pk,
        },
        {
            'section_id': 'PHY2091',
            'section_no': 1,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='T01R01R09').pk,
            'course_id': Course.objects.get(pk='PHY209').pk,
        },
        {
            'section_id': 'PHY2092',
            'section_no': 2,
            'section_capacity': 30,
            'total_students': 0,
            'instructor_id': None,
            'routine_id': WeekSlot.objects.get(pk='S01R01').pk,
            'course_id': Course.objects.get(pk='PHY209').pk,
        }
    ]

    for i in sections:
        r = Section(**i)
        r.save()

    students = [
        {
            'student_id': '2019-2-60-022',
            'name': 'Zuhair Ishraq Zareef',
            'gender': 'male',
            'advisor_id': Faculty.objects.get(faculty_id='ZI').pk,
            'username_id': User.objects.get(username='2019-2-60-022').pk
        },
        {
            'student_id': '2019-2-60-015',
            'name': 'Nusrat Maisha',
            'gender': 'female',
            'advisor_id': Faculty.objects.get(faculty_id='NM').pk,
            'username_id': User.objects.get(username='2019-2-60-015').pk
        },
        {
            'student_id': '2019-2-60-025',
            'name': 'Md. Tanvir Mobasshir',
            'gender': 'male',
            'advisor_id': Faculty.objects.get(faculty_id='TM').pk,
            'username_id': User.objects.get(username='2019-2-60-025').pk
        },
        {
            'student_id': '2018-2-60-127',
            'name': 'A. K. M. Sadat',
            'gender': 'male',
            'advisor_id': Faculty.objects.get(faculty_id='ZI').pk,
            'username_id': User.objects.get(username='2018-2-60-127').pk
        },
        {
            'student_id': '2020-1-60-226',
            'name': 'Sofia Noor Rafa',
            'gender': 'female',
            'advisor_id': Faculty.objects.get(faculty_id='NM').pk,
        },
        {
            'student_id': '2020-1-65-001',
            'name': 'Komol Kunty Rajib',
            'gender': 'male',
            'advisor_id': Faculty.objects.get(faculty_id='TM').pk,
            'username_id': User.objects.get(username='2020-1-65-001').pk
        },
        {
            'student_id': 'admin',
            'name': 'admin',
            'gender': 'male',
            'advisor_id': Faculty.objects.get(faculty_id='admin').pk,
            'username_id': User.objects.get(username='admin').pk
        }
    ]

    for i in students:
        r = Student(**i)
        r.save()

    grades = [
        {
            'grade': 'A+',
            'grade_point': 4.00,
            'maximum': 100,
            'minimum': 97,
        },
        {
            'grade': 'A',
            'grade_point': 4.0,
            'maximum': 96,
            'minimum': 90,
        },
        {
            'grade': 'A-',
            'grade_point': 3.7,
            'maximum': 89,
            'minimum': 87,
        },
        {
            'grade': 'B+',
            'grade_point': 3.3,
            'maximum': 86,
            'minimum': 83,
        },
        {
            'grade': 'B',
            'grade_point': 3.0,
            'maximum': 82,
            'minimum': 80,
        },
        {
            'grade': 'B-',
            'grade_point': 2.7,
            'maximum': 79,
            'minimum': 77,
        },
        {
            'grade': 'C+',
            'grade_point': 2.3,
            'maximum': 76,
            'minimum': 73,
        },
        {
            'grade': 'C',
            'grade_point': 2.0,
            'maximum': 72,
            'minimum': 70,
        },
        {
            'grade': 'C-',
            'grade_point': 1.7,
            'maximum': 69,
            'minimum': 67,
        },
        {
            'grade': 'D+',
            'grade_point': 1.3,
            'maximum': 66,
            'minimum': 63,
        },
        {
            'grade': 'D',
            'grade_point': 1.0,
            'maximum': 62,
            'minimum': 60,
        },
        {
            'grade': 'F',
            'grade_point': 0.0,
            'maximum': 60,
            'minimum': 0,
        },
        {
            'grade': 'W',
            'grade_point': 0.0,
            'maximum': 0,
            'minimum': 0,
        },
        {
            'grade': 'R',
            'grade_point': 0.0,
            'maximum': 0,
            'minimum': 0,
        }
    ]

    for grade in grades:
        g = Grade(**grade)
        g.save()

    grade_reports1 = [
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=4),
            'section': Section.objects.get(section_id='CSE1031'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=4),
            'section': Section.objects.get(section_id='ENG1011'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=4),
            'section': Section.objects.get(section_id='MAT1011'),
            'grade': Grade.objects.get(grade='C+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=5),
            'section': Section.objects.get(section_id='CSE1061'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=5),
            'section': Section.objects.get(section_id='ENG1021'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=5),
            'section': Section.objects.get(section_id='MAT1021'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=6),
            'section': Section.objects.get(section_id='CSE1101'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=6),
            'section': Section.objects.get(section_id='MAT1041'),
            'grade': Grade.objects.get(grade='D+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=6),
            'section': Section.objects.get(section_id='CHE1091'),
            'grade': Grade.objects.get(grade='C+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=7),
            'section': Section.objects.get(section_id='CSE2091'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=7),
            'section': Section.objects.get(section_id='GEN2261'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=7),
            'section': Section.objects.get(section_id='ECO1011'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=8),
            'section': Section.objects.get(section_id='CSE2511'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=8),
            'section': Section.objects.get(section_id='STA1021'),
            'grade': Grade.objects.get(grade='B-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=8),
            'section': Section.objects.get(section_id='PHY1091'),
            'grade': Grade.objects.get(grade='C-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='CSE2071'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='BUS2311'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='MAT2051'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=10),
            'section': Section.objects.get(section_id='CSE2461'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=10),
            'section': Section.objects.get(section_id='CSE3251'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=10),
            'section': Section.objects.get(section_id='PHY2091'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE2001'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE3021'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE3451'),
            'grade': Grade.objects.get(grade='B-')
        },
        {
            'student': Student.objects.get(student_id='2020-1-65-001'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE3601'),
            'grade': Grade.objects.get(grade='C')
        }
    ]

    for grade_report in grade_reports1:
        c = CoursesTaken(**grade_report)
        c.save()

    grade_reports2 = [
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=4),
            'section': Section.objects.get(section_id='CSE1031'),
            'grade': Grade.objects.get(grade='C-')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=4),
            'section': Section.objects.get(section_id='ENG1011'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=4),
            'section': Section.objects.get(section_id='MAT1011'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=5),
            'section': Section.objects.get(section_id='CSE1061'),
            'grade': Grade.objects.get(grade='C+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=5),
            'section': Section.objects.get(section_id='ENG1021'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=5),
            'section': Section.objects.get(section_id='MAT1021'),
            'grade': Grade.objects.get(grade='D+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=6),
            'section': Section.objects.get(section_id='CSE1101'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=6),
            'section': Section.objects.get(section_id='MAT1041'),
            'grade': Grade.objects.get(grade='R')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=6),
            'section': Section.objects.get(section_id='CHE1091'),
            'grade': Grade.objects.get(grade='B-')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=7),
            'section': Section.objects.get(section_id='CSE2091'),
            'grade': Grade.objects.get(grade='C')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=7),
            'section': Section.objects.get(section_id='GEN2261'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=7),
            'section': Section.objects.get(section_id='ECO1011'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=8),
            'section': Section.objects.get(section_id='CSE2511'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=8),
            'section': Section.objects.get(section_id='STA1021'),
            'grade': Grade.objects.get(grade='B-')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=8),
            'section': Section.objects.get(section_id='PHY1091'),
            'grade': Grade.objects.get(grade='C+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='CSE2071'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='BUS2311'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='MAT2051'),
            'grade': Grade.objects.get(grade='A-')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=9),
            'section': Section.objects.get(section_id='MAT1041'),
            'grade': Grade.objects.get(grade='C')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=10),
            'section': Section.objects.get(section_id='CSE2461'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=10),
            'section': Section.objects.get(section_id='CSE3251'),
            'grade': Grade.objects.get(grade='B-')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=10),
            'section': Section.objects.get(section_id='PHY2091'),
            'grade': Grade.objects.get(grade='B')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE2001'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE3021'),
            'grade': Grade.objects.get(grade='A')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE3451'),
            'grade': Grade.objects.get(grade='B+')
        },
        {
            'student': Student.objects.get(student_id='2019-2-60-022'),
            'semester': Semester.objects.get(semester_id=11),
            'section': Section.objects.get(section_id='CSE3601'),
            'grade': Grade.objects.get(grade='B-')
        }
    ]

    for grade_report in grade_reports2:
        c = CoursesTaken(**grade_report)
        c.save()

    return HttpResponse('Done')
