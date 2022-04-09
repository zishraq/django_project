from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Department(models.Model):
    department_id = models.CharField(max_length=100, primary_key=True)
    department_name = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Course(models.Model):
    course_id = models.CharField(max_length=100, primary_key=True)
    course_code = models.CharField(max_length=10)
    course_title = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    prerequisite_course = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    credit = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Semester(models.Model):
    semester_id = models.IntegerField(primary_key=True)
    semester_name = models.TextField()
    semester_starts_on = models.DateField()
    semester_ends_on = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    advising_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.advising_status:
            try:
                temp = Semester.objects.get(advising_status=True)
                if self != temp:
                    temp.is_the_chosen_one = False
                    temp.save()
            except Semester.DoesNotExist:
                pass
        super(Semester, self).save(*args, **kwargs)


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=30)
    initials = models.TextField()
    username = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


class Student(models.Model):
    student_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=30)
    advisor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    username = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


class WeekSlot(models.Model):
    routine_id = models.CharField(max_length=100, primary_key=True)


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
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creator')
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updater')


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
    course_record_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    # semester = models.ForeignKey(StudentRecordsBySemester, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)


class SectionsRequested(models.Model):
    request_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    # semester = models.ForeignKey(StudentRecordsBySemester, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    approved_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

