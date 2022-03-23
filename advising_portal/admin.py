from django.contrib import admin
from .models import Department, Course, Faculty, Student, Section, Semester, CoursesTaken, TimeSlot, RoutineSlot

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(TimeSlot)
admin.site.register(RoutineSlot)
admin.site.register(Section)
admin.site.register(Semester)
admin.site.register(CoursesTaken)
