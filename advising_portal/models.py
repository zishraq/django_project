from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Department(models.Model):
    department_id = models.CharField(max_length=100)
    # department_name =



class Courses(models.Model):
    course_code = models.CharField(max_length=100)
    course_title = models.CharField(max_length=100)

    def __str__(self):
        return self.course_title