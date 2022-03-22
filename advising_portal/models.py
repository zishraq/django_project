from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Department(models.Model):
    department_id = models.CharField(max_length=100, primary_key=True)
    department_name = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Course(models.Model):
    course_id = models.CharField(max_length=100, primary_key=True)
    course_code = models.CharField(max_length=10)
    course_title = models.TextField()
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    prerequisite_course_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    credit = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Semester(models.Model):
    semester_id = models.CharField(max_length=100, primary_key=True)
    semester_starts_on = models.DateField()
    semester_ends_on = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=100, primary_key=True)
    name = models.TextField()
    initials = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Student(models.Model):
    student_id = models.CharField(max_length=100, primary_key=True)
    name = models.TextField()
    advisor = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class TimeSlot(models.Model):
    time_slot_id = models.CharField(max_length=100, primary_key=True)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.day} {str(self.start_time)} - {str(self.start_time)}'


class RoutineSlot(models.Model):
    routine_id = models.CharField(max_length=100, primary_key=True)
    time_slot_id = models.ForeignKey(TimeSlot, on_delete=models.DO_NOTHING, null=True)
    # time_slot_id = models.ManyToManyField(TimeSlot)


class Section(models.Model):
    section_id = models.CharField(max_length=100, primary_key=True)
    section_no = models.PositiveIntegerField(default=1)
    section_capacity = models.PositiveIntegerField(default=0)
    total_students = models.PositiveIntegerField(default=0)
    instructor_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    routine_id = models.ForeignKey(RoutineSlot, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)


class CoursesTaken(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester_id = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    section_id = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    grade = models.FloatField()
