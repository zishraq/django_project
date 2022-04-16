from django.contrib import admin
from .models import Department, Course, Faculty, Student, Section, Semester, CoursesTaken, TimeSlot, WeekSlot, Grade, Routine, SectionsRequested

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(TimeSlot)
admin.site.register(WeekSlot)
admin.site.register(Routine)
admin.site.register(Section)
admin.site.register(Semester)
admin.site.register(CoursesTaken)
admin.site.register(SectionsRequested)
admin.site.register(Grade)
