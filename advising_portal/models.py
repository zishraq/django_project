import re
from datetime import datetime
from PIL import Image

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

from advising_portal.utilities import ADDED, DROPPED, PENDING, APPROVED, REJECTED


class Department(models.Model):
    department_id = models.CharField(max_length=100, primary_key=True)
    department_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='department_creator')
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='department_updater')
    chairman = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='department_chairman')
    history = HistoricalRecords()

    def __str__(self):
        return self.department_name


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    semester_name = models.CharField(max_length=50, validators=[RegexValidator(r'(Spring|Summer|Fall)\-[0-9]{4}')])
    semester_starts_at = models.DateField()
    semester_ends_at = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='semester_creator')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='semester_updater')
    advising_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    add_drop_status = models.BooleanField(default=False)
    seat_request_status = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.semester_name

    def save(self, *args, **kwargs):
        if self.advising_status:
            try:
                temp = Semester.objects.get(advising_status=True)
                if self != temp:
                    temp.advising_status = False
                    temp.save()
            except Semester.DoesNotExist:
                pass

        if self.is_active:
            try:
                temp = Semester.objects.get(is_active=True)
                if self != temp:
                    temp.is_active = False
                    temp.save()
            except Semester.DoesNotExist:
                pass

        if self.add_drop_status:
            try:
                temp = Semester.objects.get(add_drop_status=True)
                if self != temp:
                    temp.add_drop_status = False
                    temp.save()
            except Semester.DoesNotExist:
                pass

        if self.seat_request_status:
            try:
                temp = Semester.objects.get(add_drop_status=True)
                if self != temp:
                    temp.add_drop_status = False
                    temp.save()
            except Semester.DoesNotExist:
                pass

        super(Semester, self).save(*args, **kwargs)


class Course(models.Model):
    course_id = models.CharField(max_length=100, primary_key=True)
    course_code = models.CharField(max_length=10)
    course_title = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='related_department')
    prerequisite_course = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='related_prerequisite_course')
    credit = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='related_created_by')
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, related_name='related_semester')
    history = HistoricalRecords()

    def __str__(self):
        return self.course_code


# class CourseBySemester(models.Model):
#     semester_course_id = models.CharField(max_length=100, primary_key=True)
#     semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, related_name='semester')
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='semester')


# class CoursePrerequisites(models.Model):
#     class Meta:
#         unique_together = (('course_code', 'prerequisite_course_code'),)
#
#     course_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_code')
#     prerequisite_course_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisite_course_code')


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=30)
    initials = models.CharField(max_length=10)
    profile_picture = models.ImageField(default='male_default.svg', upload_to='profile_pictures')
    gender = models.CharField(max_length=10, validators=[RegexValidator(r'(male|female|other)')])
    username = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.initials

    def save(self, *args, **kwargs):
        if self.gender == 'male':
            self.profile_picture = 'male_default.svg'

        else:
            self.profile_picture = 'female_default.svg'

        super(Faculty, self).save(*args, **kwargs)


class Student(models.Model):
    student_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=30)
    advisor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    gender = models.CharField(max_length=10, validators=[RegexValidator(r'(male|female|other)')])
    username = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # if self.gender == 'male':
        #     self.profile_picture = 'male_default.svg'
        #
        # else:
        #     self.profile_picture = 'female_default.svg'

        # self.profile_picture = 'default.jpg'

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

        super(Student, self).save(*args, **kwargs)


class WeekSlot(models.Model):
    routine_id = models.CharField(max_length=100, primary_key=True)

    def get_time_slots_of_week_slot(self):
        routine_slot_chunks = [self.routine_id[i:i + 3] for i in range(0, len(self.routine_id), 3)]
        return routine_slot_chunks

    def is_valid_week_slot(self):
        if not re.match('^([A-Z]\d{2}){1,3}$', self.routine_id):
            return False

        time_slots_of_week_slot = self.get_time_slots_of_week_slot()
        time_slot_objects = []

        for time_slot in time_slots_of_week_slot:
            if not TimeSlot.objects.filter(time_slot_id=time_slot).exists():
                return False

            time_slot_object = TimeSlot.objects.get(time_slot_id=time_slot)
            time_slot_objects.append(time_slot_object)

        for time_slot1 in range(len(time_slot_objects)):
            for time_slot2 in range(len(time_slot_objects)):
                if time_slot1 != time_slot2:
                    if time_slot_objects[time_slot1].does_conflict_with_time_slot(time_slot_objects[time_slot2]):
                        return False

        return True

    def save(self, *args, **kwargs):
        if self.is_valid_week_slot():
            super(WeekSlot, self).save(*args, **kwargs)

        else:
            raise Exception('Invalid week slot')

    def __str__(self):
        get_time_slots = Routine.objects.filter(
            routine_slot_id=self.routine_id
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

        return routine_str


class TimeSlot(models.Model):
    time_slot_id = models.CharField(max_length=100, primary_key=True)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        time_visual_format = f'{self.day} {self.start_time.strftime("%I:%M %p")}-{self.end_time.strftime("%I:%M %p")}'

        if time_visual_format[8:10] == time_visual_format[17:19]:
            time_visual_format = time_visual_format[:7] + time_visual_format[10:19]

        return time_visual_format

    def does_conflict_with_time_slot(self, compare_time_slot):
        if self.day == compare_time_slot.day:
            this_time_slot_start_time = datetime.strptime(str(self.start_time), '%H:%M:%S')
            this_time_slot_end_time = datetime.strptime(str(self.end_time), '%H:%M:%S')

            compare_time_slot_start_time = datetime.strptime(str(compare_time_slot.start_time), '%H:%M:%S')
            compare_time_slot_end_time = datetime.strptime(str(compare_time_slot.end_time), '%H:%M:%S')

            if this_time_slot_end_time == compare_time_slot_end_time:
                return True

            elif this_time_slot_start_time == compare_time_slot_start_time:
                return True

            elif this_time_slot_start_time < compare_time_slot_end_time < this_time_slot_end_time:
                return True

            elif compare_time_slot_start_time < this_time_slot_end_time < compare_time_slot_end_time:
                return True

        return False


class Routine(models.Model):
    routine_slot = models.ForeignKey(WeekSlot, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)


class Section(models.Model):
    section_id = models.CharField(max_length=100, primary_key=True)
    section_no = models.PositiveIntegerField(default=1)
    section_capacity = models.PositiveIntegerField(default=0)
    total_students = models.PositiveIntegerField(default=0)
    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    routine = models.ForeignKey(WeekSlot, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='section_by_course', related_query_name='section_course')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='section_creator')
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='section_updater')
    history = HistoricalRecords()

    def does_conflict_with_section(self, compare_section):
        time_slots_of_current_section = Routine.objects.filter(routine_slot=self.routine)

        compare_section_routine = compare_section.routine  # Get routine id of the comparing section
        time_slots_of_compare_section = Routine.objects.filter(
            routine_slot=compare_section_routine
        )  # Get time slots of current section

        # Check for time slot conflict
        for i in time_slots_of_compare_section:
            for j in time_slots_of_current_section:
                if i.time_slot.does_conflict_with_time_slot(j.time_slot):
                    return True

        return False


class Grade(models.Model):
    grade = models.CharField(max_length=10, primary_key=True)
    grade_point = models.FloatField()
    maximum = models.FloatField()
    minimum = models.FloatField()


# class StudentRecordsBySemester(models.Model):
#     semester_record_id = models.AutoField(primary_key=True)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
#     term_gpa = models.FloatField()
#     current_cgpa = models.FloatField()
#     total_credits = models.FloatField()


class CoursesTaken(models.Model):
    STATUS = (
        (ADDED, ADDED),
        (DROPPED, DROPPED)
    )

    course_record_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    # semester = models.ForeignKey(StudentRecordsBySemester, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)

    added_at = models.DateTimeField(default=datetime.now())
    dropped_at = models.DateTimeField(default=None, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default=ADDED)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='adder')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updater')


class SectionsRequested(models.Model):
    APPROVAL_STATUS = (
        (PENDING, PENDING),
        (APPROVED, APPROVED),
        (REJECTED, REJECTED)
    )

    request_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    # semester = models.ForeignKey(StudentRecordsBySemester, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default=PENDING)

    advisor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='advisor')
    advisor_approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default=PENDING)
    advisor_text = models.TextField()

    chairman = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='chairman')
    chairman_approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default=PENDING)
    chairman_text = models.TextField()

    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='instructor')
    instructor_approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default=PENDING)
    instructor_text = models.TextField()

    requested_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=None, null=True)
