import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.models import LogEntry, ADDITION

from advising_portal.forms import SectionRequestForm, CreateCourseForm, CreateSemesterForm, UpdateSectionForm, \
    CreateSectionForm
from advising_portal.models import Course, Section, CoursesTaken, Semester, Student, Routine, TimeSlot, WeekSlot, \
    SectionsRequested, Grade, Faculty
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
    return render(request, 'advising_portal/base.html')


@login_required
@allowed_users(allowed_roles=['student'])
def advising_portal_list_view(request, section_filter):
    student = Student.objects.get(username_id=request.user)

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
        semester_id=current_semester_id
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
        'form': form
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
                        # 'grade_point': course.grade.grade_point,
                        'grade_point': grade_point,
                    }
                ],
                'current_cgpa': total_cgpa,
                'current_total_credit': total_credit,
                # 'term_gpa': course.grade.grade_point * course_credit
                'term_gpa': grade_point * course_credit
            }

        else:
            courses_by_semesters[course.semester_id]['total_credit'] += course_credit
            courses_by_semesters[course.semester_id]['current_cgpa'] = total_cgpa
            courses_by_semesters[course.semester_id]['current_total_credit'] = total_credit
            # courses_by_semesters[course.semester_id]['term_gpa'] += (course.grade.grade_point * course_credit)
            courses_by_semesters[course.semester_id]['term_gpa'] += (grade_point * course_credit)
            courses_by_semesters[course.semester_id]['courses'].append(
                {
                    'course_code': course_code,
                    'course_title': re.sub('\(.*\)', '', str(course.section.course.course_title)),
                    'course_credit': course_credit,
                    'grade': letter_grade,
                    'total_gp': course_credit * 4,
                    # 'grade_point': course.grade.grade_point,
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
        'maximum_grade_frequency': max(list(grade_frequency.values())) + 3
    }

    return render(request, 'advising_portal/grading_report.html', context)


@login_required
@allowed_users(allowed_roles=['student'])
def advised_course_list_view(request):
    student_id = Student.objects.get(username_id=request.user).pk
    semester_id = request.GET.get('semester_id', '')

    if not semester_id:
        semester_id = Semester.objects.get(advising_status=True).pk

    semester = Semester.objects.get(semester_id=semester_id)

    semesters = list(Semester.objects.all().order_by('-semester_id'))

    courses_taken = CoursesTaken.objects.filter(
        student_id=student_id,
        semester_id=semester.semester_id
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
        'is_advising_semester': semester.advising_status
    }

    return render(request, 'advising_portal/advised_course_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_list_view(request):
    courses = Course.objects.all()
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
        'courses': course_list
    }

    return render(request, 'advising_portal/course_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_detail_view(request, course_id):
    course_data = Course.objects.get(
        course_id=course_id
    )

    print(course_data.history.all())

    if request.method == 'POST':
        form = CreateCourseForm(request.POST, instance=course_data)

        if form.is_valid():
            # create_course_data = form.cleaned_data
            # create_course_data['course_id'] = create_course_data['course_code']
            #
            # new_course = Course(**create_course_data)
            # new_course.save()

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

    print(course_data.course_code)

    context = {
        'form': form,
        'sections': section_list,
        'course_code': course_data.course_code,
        'course_id': course_data.course_id
    }

    return render(request, 'advising_portal/course_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def course_create_view(request):
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
        'section_id': section_data.section_id
    }

    return render(request, 'advising_portal/section_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def section_create_view(request, course_code):
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
        'semesters': semester_list
    }

    return render(request, 'advising_portal/semester_list.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def semester_detail_view(request, semester_id):
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
        'form': form
    }

    return render(request, 'advising_portal/semester_detail.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def semester_create(request):
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
    }

    return render(request, 'advising_portal/create_semester.html', context)


@login_required
@allowed_users(allowed_roles=['faculty'])
def assigned_sections(request):
    get_faculty = Faculty.objects.get(username=request.user)

    instructors_sections = Section.objects.filter(
        instructor=get_faculty
    )

    print(instructors_sections)

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
    }

    return render(request, 'advising_portal/assigned_section_list.html', context)
