import re
from datetime import datetime
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django.apps import apps
from django.contrib.admin.models import LogEntry, ADDITION

from advising_portal.forms import SectionRequestForm, CreateCourseForm, CreateSemesterForm, UpdateSectionForm, \
    CreateSectionForm, UpdateSectionRequestForm, FacultyStudentUpdateForm
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student, Routine, TimeSlot, WeekSlot, \
    SectionsRequested, Grade, Faculty
from django.contrib.auth.decorators import login_required

from advising_portal.utilities import student_id_regex, ADDED, DROPPED, get_referer_parameter, \
    get_conflicting_sections_with_requested_section, text_shorten, APPROVED, REJECTED, PENDING
from notification_system.models import BroadcastNotification
from users.decorators import allowed_users


@login_required
def home(request):
    user_id = request.user.id

    context = {
        'room_name': str(user_id)
    }
    return render(request, 'advising_portal/base.html', context)


@login_required
@allowed_users(allowed_roles=['student', 'faculty', 'chairman'])
def advising_portal_list_view(request, section_filter):
    if request.user.groups.all()[0].name == 'chairman' or request.user.groups.all()[0].name == 'faculty':
        student_id = request.GET.get('student_id', '')

        student = Student.objects.get(
            student_id=student_id
        )
    else:
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
            course__course_code__in=Section.objects.filter(
                section_id__in=get_previous_selected_sections
            ).values('course__course_code').all()
        )

        ### exclude courses without pre-requisite completion
        sections = sections.exclude(
            course__course_code__in=Course.objects.filter(
                prerequisite_course__course_code__in=Section.objects.exclude(
                    section_id__in=get_previous_selected_sections
                ).values('course__course_code').all()
            ).values('course_code').all()
        )

    elif section_filter == 'retakable':
        sections = Section.objects.filter(
            course__course_code__in=Section.objects.filter(
                section_id__in=CoursesTaken.objects.filter(
                    student_id=student,
                    grade_id__in=['C', 'C+', 'C-']
                ).values('section_id').all()
            ).values('course__course_code').all()
        ).order_by('course__course_code')

    elif section_filter == 'f':
        sections = Section.objects.filter(
            course__course_code__in=Section.objects.filter(
                section_id__in=CoursesTaken.objects.filter(
                    student_id=student,
                    grade_id__in=['F']
                ).values('section_id').all()
            ).values('course__course_code').all()
        ).order_by('course__course_code')

    else:
        d_courses = CoursesTaken.objects.filter(
            student_id=student,
            grade_id__in=['D+', 'D']
        ).values('section_id').all()

        get_course_ids = Section.objects.filter(
            section_id__in=d_courses
        ).values('course__course_code').all()

        sections = Section.objects.filter(
            course__course_code__in=get_course_ids
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

    if request.user.groups.all()[0].name == 'chairman' or request.user.groups.all()[0].name == 'faculty':
        student_id = request.GET.get('student_id', '')
    else:
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
        'student': student,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/portal.html', context)


@login_required
@allowed_users(allowed_roles=['student', 'faculty', 'chairman'])
def add_course_view(request, section_id):
    referer_parameter = get_referer_parameter(request)

    current_semester = Semester.objects.get(advising_status=True)  # get current semester

    user_group = request.user.groups.all()[0].name

    if user_group in ['chairman', 'faculty']:
        student_id = request.GET.get('student_id', '')

        student = Student.objects.get(
            student_id=student_id
        )
    else:
        student = Student.objects.get(username_id=request.user)  # get User's student info

    selected_section = Section.objects.get(section_id=section_id)  # get selected section data
    selected_course = selected_section.course  # get course data of the selected section

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

    if user_group in ['chairman', 'faculty']:
        base_url = reverse('student-panel-portal', kwargs={'section_filter': referer_parameter})

        query_string = urlencode(
            {
                'student_id': student.student_id
            }
        )
        redirect_url = '{}?{}'.format(base_url, query_string)
        return redirect(redirect_url)

    return redirect('student-panel-portal', referer_parameter)


@login_required
@allowed_users(allowed_roles=['student', 'faculty', 'chairman'])
def drop_course_view(request, section_id):
    user_group = request.user.groups.all()[0].name

    if user_group in ['chairman', 'faculty']:
        student_id = request.GET.get('student_id', '')

        # if not student_id:
        #     return render(request, 'advising_portal/401.html')

    else:
        student_id = Student.objects.get(username_id=request.user).student_id

    referer_parameter = get_referer_parameter(request)
    current_time = timezone.now()

    current_semester_id = Semester.objects.get(advising_status=True).semester_id
    selected_section = Section.objects.get(section_id=section_id)

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

    if user_group in ['chairman', 'faculty']:
        base_url = reverse('student-panel-portal', kwargs={'section_filter': referer_parameter})

        query_string = urlencode(
            {
                'student_id': student_id
            }
        )
        redirect_url = '{}?{}'.format(base_url, query_string)
        return redirect(redirect_url)

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

    current_semester = Semester.objects.get(advising_status=True)  # get current semester
    student = Student.objects.get(username_id=request.user)  # get User's student info

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
            'conflicting_sections': conflicting_sections['conflicting_sections'],
        }

        view_section_data.append(formatted_data)

    student_id = Student.objects.get(username_id=request.user).pk
    current_semester_id = Semester.objects.get(advising_status=True).pk

    sections_requested = SectionsRequested.objects.filter(
        student_id=student_id,
        semester_id=current_semester_id,
        status=PENDING
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
    current_semester = Semester.objects.get(advising_status=True)  # get current semester
    student = Student.objects.get(username_id=request.user)  # get User's student info
    requested_section = Section.objects.get(section_id=section_id)  # get selected section data
    requested_course = requested_section.course  # get course data of the selected section

    requested_section_routine_id = requested_section.routine_id  # store routine id of the selected section
    time_slots_of_requested_section = Routine.objects.filter(
        routine_slot_id=requested_section_routine_id)  # get time slots by routine id

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
    messages.success(request,
                     f'Successfully requested for Section-{requested_section.section_no} of {requested_section.course.course_code}')
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

    messages.success(request,
                     f'Request removed for Section-{selected_section.section_no} of {selected_section.course.course_code}')
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

    semesters = list(Semester.objects.all())

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
@allowed_users(allowed_roles=['faculty', 'chairman'])
def course_list_view(request):
    semester_id = request.GET.get('semester_id', '')

    if not semester_id:
        semester_id = Semester.objects.get(advising_status=True).pk

    semester = Semester.objects.get(semester_id=semester_id)

    semesters = list(Semester.objects.all())

    courses = Course.objects.filter(
        semester=semester
    )
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
        'semester_name': semester.semester_name,
        'semesters': semesters,
        'room_name': str(user_id),
        'semester_id': semester_id
    }

    return render(request, 'advising_portal/course_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
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
            return redirect('faculty-panel-course-detail', course_id)

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
@allowed_users(allowed_roles=['faculty', 'chairman'])
def course_create_view(request):
    user_id = request.user.id

    if request.method == 'POST':
        form = CreateCourseForm(request.POST)

        if form.is_valid():
            create_course_data = form.cleaned_data

            create_course_data['course_id'] = str(create_course_data['semester'].semester_id) + create_course_data[
                'course_code']
            create_course_data['created_by_id'] = user_id
            new_course = Course(**create_course_data)
            new_course.save()

            messages.success(request, 'Course successfully created!')
            return redirect('faculty-panel-course-list')

    else:
        form = CreateCourseForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/create_course.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def course_log_view(request, course_id):
    HistoricalCourse = apps.get_model('advising_portal', 'HistoricalCourse')
    courses_data = HistoricalCourse.objects.filter(
        course_id=course_id
    )

    course_log = []

    for data in courses_data:
        formatted_data = {
            'course_id': data.course_id,
            'course_code': data.course_code,
            'created_at': data.history_date,
            'created_by': data.created_by,
            'semester': data.semester
        }
        if data.history_type == '+':
            formatted_data['history_type'] = 'added'
        elif data.history_type == '-':
            formatted_data['history_type'] = 'deleted'
        else:
            formatted_data['history_type'] = 'updated'

        course_log.append(formatted_data)

    context = {'course_log': course_log}

    return render(request, 'advising_portal/course_log.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def semester_log_view(request, semester_id):
    HistoricalSemester = apps.get_model('advising_portal', 'HistoricalSemester')
    semester_data = HistoricalSemester.objects.filter(
        semester_id=semester_id
    )

    semester_log = []

    for data in semester_data:
        formatted_data = {
            'semester_id': data.semester_id,
            'semester_name': data.semester_name,
            'created_at': data.updated_at,
            'created_by': data.updated_by
        }
        if data.history_type == '+':
            formatted_data['history_type'] = 'added'
        elif data.history_type == '-':
            formatted_data['history_type'] = 'deleted'
        else:
            formatted_data['history_type'] = 'updated'

        semester_log.append(formatted_data)

    context = {'semester_log': semester_log}

    return render(request, 'advising_portal/semester_log.html', context)



@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def course_delete_view(request, course_id):
    course_data = Course.objects.get(course_id=course_id)

    Course.objects.filter(
        course_id=course_id
    ).delete()

    messages.success(request, f'Deleted course {course_data.course_code}')
    return redirect('student-panel-course-list')



@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def semester_delete_view(request, semester_id):
    course_data = Semester.objects.get(semester_id=semester_id)

    Semester.objects.filter(
        semester_id=semester_id
    ).delete()

    messages.success(request, f'Deleted Semester {course_data.semester_id}')
    return redirect('faculty-panel-semester-list')


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
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
                    messages.error(request,
                                   f'Instructor assigned to Section-{section.section_no} of Course {section.course.course_code}!')
                    return redirect('faculty-panel-section-detail', section_id)

            form.save()

            messages.success(request, 'Section successfully updated!')
            return redirect('faculty-panel-course-detail', section_data.course_id)

    else:
        form = UpdateSectionForm(instance=section_data)

    students = Student.objects.filter(
        student_id__in=CoursesTaken.objects.filter(
            section__course__course_code=section_data.course.course_code,
        ).values('student__student_id')
    )

    student_list = []

    for student in students:
        formatted_data = {
            'student_id': student.student_id,
            'name': student.name,
            'advisor': student.advisor.name,
        }

        student_list.append(formatted_data)

    context = {
        'form': form,
        'course_code': section_data.course.course_code,
        'students': students,
        'section_no': section_data.section_no,
        'section_id': section_data.section_id,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
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
            return redirect('faculty-panel-course-detail', course_code)

    else:
        form = CreateSectionForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_create.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def section_delete_view(request, section_id):
    section_data = Section.objects.get(section_id=section_id)

    Section.objects.filter(
        section_id=section_id
    ).delete()

    messages.success(request, f'Deleted section-{section_data.section_no} of course {section_data.course.course_code}')
    return redirect('faculty-panel-course-detail', section_data.course.course_code)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def semester_list_view(request):
    user_id = request.user.id
    semesters = Semester.objects.all()
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
@allowed_users(allowed_roles=['faculty', 'chairman'])
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

            semester_data.update(update_semester_data)
            semester_data.save()

            messages.success(request, 'Semester successfully updated!')
            return redirect('faculty-panel-semester-list')

    else:
        form = CreateSemesterForm(instance=semester_data)

    context = {
        'form': form,
        'room_name': str(user_id),
        'semester_id': semester_id
    }

    return render(request, 'advising_portal/semester_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
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
            return redirect('faculty-panel-semester-list')

    else:
        form = CreateSemesterForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/create_semester.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
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
@allowed_users(allowed_roles=['faculty', 'chairman'])
def section_request_list_view(request):
    user_id = request.user.id
    user = request.user

    if user.groups.filter(name='chairman'):
        section_requests = SectionsRequested.objects.filter(
            section__course__department__chairman=user
        )

    else:
        section_requests = SectionsRequested.objects.filter(
            Q(student__advisor__username_id=user_id) | Q(section__instructor__username=user_id)
        )

    section_requests_list = []

    for section_request in section_requests:
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
@allowed_users(allowed_roles=['faculty', 'chairman'])
def section_request_detail_view(request, request_id):
    current_time = timezone.now()
    user_id = request.user.id

    section_request_data = SectionsRequested.objects.get(
        request_id=request_id
    )

    requested_section_data = section_request_data.section

    current_faculty_data = Faculty.objects.get(
        username__id=user_id
    )

    student_advisor = section_request_data.student.advisor.username
    department_chairman = section_request_data.section.course.department.chairman

    if request.method == 'POST':
        form = UpdateSectionRequestForm(request.POST)

        if form.is_valid():
            update_semester_data = form.cleaned_data

            if update_semester_data['approval_status'] == REJECTED:
                section_request_data.status = REJECTED
                section_request_data.save()

                messages.success(request, 'Request rejected!')
                return redirect('faculty-panel-section-request-list')

            if current_faculty_data.username == student_advisor:
                section_request_data.advisor = current_faculty_data
                section_request_data.advisor_approval_status = update_semester_data['approval_status']
                section_request_data.advisor_text = update_semester_data['text']

            if section_request_data.section.instructor:
                section_instructor = section_request_data.section.instructor.username

                if current_faculty_data.username == section_instructor:
                    section_request_data.instructor = current_faculty_data
                    section_request_data.instructor_approval_status = update_semester_data['approval_status']
                    section_request_data.instructor_text = update_semester_data['text']

            else:
                section_request_data.instructor_approval_status = APPROVED

            if current_faculty_data.username == department_chairman:
                section_request_data.chairman = current_faculty_data
                section_request_data.chairman_approval_status = update_semester_data['approval_status']
                section_request_data.chairman_text = update_semester_data['text']

            course_added = False

            if section_request_data.advisor_approval_status == section_request_data.instructor_approval_status == section_request_data.chairman_approval_status == APPROVED:
                previous_selected_sections = CoursesTaken.objects.filter(
                    student=section_request_data.student,
                    semester=section_request_data.semester,
                    status=ADDED
                ).all()

                conflicting_sections = get_conflicting_sections_with_requested_section(
                    previous_selected_sections=previous_selected_sections,
                    selected_section=requested_section_data
                )

                for section_id in conflicting_sections['section_ids']:
                    section_to_drop = CoursesTaken(
                        student=section_request_data.student,
                        semester=section_request_data.semester,
                        section_id=section_id,
                        status=ADDED
                    )

                    section_to_drop.dropped_at = current_time
                    section_to_drop.status = DROPPED
                    section_to_drop.updated_by = request.user
                    section_to_drop.save()

                course_selected = CoursesTaken(
                    student=section_request_data.student,
                    semester=section_request_data.semester,
                    section=requested_section_data,
                    status=ADDED
                )
                course_selected.save()
                section_request_data.status = APPROVED
                course_added = True

            section_request_data.save()

            if course_added:
                notification = BroadcastNotification(
                    message='Your course has been added',
                    broadcast_at=timezone.now() + timezone.timedelta(minutes=1),
                    notification_to=section_request_data.student.username
                )
                notification.save()

                messages.success(request, 'Course Added!')
            else:
                messages.success(request, 'Approval submitted!')

            return redirect('faculty-panel-section-request-list')

    else:
        form = UpdateSectionRequestForm()

    context = {
        'form': form,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/section_request_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def student_list_view(request):
    user_id = request.user.id
    students = Student.objects.all()
    student_list = []

    print(request.user.groups.all()[0].name)

    if 'chairman' in request.user.groups.all()[0].name:
        print('chairman')

    for student in students:
        formatted_data = {
            'student_id': student.student_id,
            'student_name': student.name,
            'advisor': student.advisor.name,
            'gender': student.gender
        }
        student_list.append(formatted_data)

    context = {
        'students': student_list,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/student_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty', 'chairman'])
def student_detail_view(request, student_id):
    user_id = request.user.id

    student_data = Student.objects.get(
        student_id=student_id
    )

    if request.method == 'POST':
        form = FacultyStudentUpdateForm(request.POST, instance=student_data)

        if form.is_valid():
            update_student_data = form.cleaned_data
            update_student_data['updated_at'] = timezone.now()
            update_student_data['updated_by'] = request.user

            updated_student = Student(**update_student_data)
            updated_student.save()

            messages.success(request, 'Student successfully updated!')
            return redirect('faculty-panel-student-list')

    else:
        form = FacultyStudentUpdateForm(instance=student_data)

    semester_id = request.GET.get('semester_id', '')

    if not semester_id:
        semester_id = Semester.objects.get(advising_status=True).pk

    semester = Semester.objects.get(semester_id=semester_id)

    semesters = list(Semester.objects.all())

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
        'form': form,
        'student_id': student_id,
        'selected_courses': view_selected_courses_data,
        'portal_type': 'course_advising',
        'semesters': semesters,
        'is_advising_semester': semester.advising_status,
        'room_name': str(user_id)
    }

    return render(request, 'advising_portal/student_detail.html', context)


def insert_test_data(request):
    from advising_portal.models import WeekSlot, TimeSlot, Routine, Department, Course, Faculty, Section, Student, \
        Semester, Grade, CoursesTaken
    from django.contrib.auth.models import User, Group
    from advising_portal.resources.groups import user_groups
    from advising_portal.resources.project_users import project_users

    for g in user_groups:
        group = Group.objects.create(**g)
        group.save()

    for u in project_users:
        user = User.objects.create_user(**u)
        user.save()

        if re.match(student_id_regex, user.username):
            group = Group.objects.get(name='student')
            group.user_set.add(user)

        elif user.username in ['nusrat', 'tanvir']:
            group = Group.objects.get(name='chairman')
            group.user_set.add(user)

        else:
            group = Group.objects.get(name='faculty')
            group.user_set.add(user)

    from advising_portal.resources.department import departments

    for i in departments:
        print(i)

        r = Department(**i)
        r.save()

    from advising_portal.resources.semester import semesters

    for i in semesters:
        print(i)

        r = Semester(**i)
        r.save()

    from advising_portal.resources.course import courses

    for s in semesters:
        for i in courses:
            # r = Course(**i)
            # r.save()

            semester_id = Semester.objects.get(pk=s['semester_id']).pk

            formatted_data = {
                'semester_id': semester_id,
                'course_id': str(semester_id) + i['course_id'],
                'course_code': i['course_code'],
                'course_title': i['course_title'],
                'department_id': i['department_id'],
                'prerequisite_course_id': str(semester_id) + i['prerequisite_course_id'] if i[
                    'prerequisite_course_id'] else None,
                'credit': i['credit'],
                'created_by_id': i['created_by_id']
            }

            print(formatted_data)

            try:
                r = Course(**formatted_data)
                r.save()

            except:
                print('fail=', formatted_data)

    from advising_portal.resources.faculty import faculties

    for i in faculties:
        print(i)
        r = Faculty(**i)
        r.save()

    from advising_portal.resources.time_slot import time_slots

    for i in time_slots.values():
        print(i)
        t = TimeSlot(**i)
        t.save()

    from advising_portal.resources.routine import routine_slot

    for i in routine_slot:
        print(i)
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

    from advising_portal.resources.section import sections

    for s in semesters:
        for i in sections:
            formatted_data = {
                'section_id': str(s['semester_id']) + i['section_id'],
                'section_no': i['section_no'],
                'section_capacity': i['section_capacity'],
                'total_students': i['total_students'],
                'instructor_id': i['instructor_id'],
                'routine_id': i['routine_id'],
                'course_id': str(s['semester_id']) + i['course_id']
            }

            print(formatted_data)

            r = Section(**formatted_data)
            r.save()

        # r = Section(**i)
        # r.save()

    from advising_portal.resources.student import students

    for i in students:
        print(i)

        r = Student(**i)
        r.save()

    from advising_portal.resources.grades import grades

    for grade in grades:
        print(grade)

        g = Grade(**grade)
        g.save()

    from advising_portal.resources.grade_report import updated_grade_report1, updated_grade_report2

    for grade_report in updated_grade_report1:
        print(grade_report)

        c = CoursesTaken(**grade_report)
        c.save()

    for grade_report in updated_grade_report2:
        print(grade_report)

        c = CoursesTaken(**grade_report)
        c.save()

    return HttpResponse('Done')
