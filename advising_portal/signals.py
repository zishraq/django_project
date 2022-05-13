from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
# from .models import Student
from advising_portal.models import Section, CoursesTaken
from advising_portal.utilities import ADDED


@receiver(post_save, sender=CoursesTaken)
def select_course(sender, instance, created, **kwargs):
    if created:
        section_data = instance.section
        section_data.total_students += 1
        section_data.save()

    else:
        if instance.status == ADDED:
            if instance.student.username != instance.added_by:
                if instance.section_capacity == instance.total_students:
                    instance.section_capacity = instance.section_capacity + 1

            else:
                section_data = instance.section
                section_data.total_students += 1
                section_data.save()

        else:
            section_data = instance.section
            section_data.total_students -= 1
            section_data.save()
