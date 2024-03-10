from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        # Fetch all students enrolled in the course
        enrollments = Enrollment.objects.filter(course=course)
        for enrollment in enrollments:
            # Create a notification for each student
            Notification.objects.create(
                recipient=enrollment.student,
                message=f'A new post "{instance.title}" has been added to your course: {course.title}.'
            )

@receiver(post_save, sender=Enrollment)
def enrollment_created(sender, instance, created, **kwargs):
    if created:
        teacher = instance.course.teacher
        # Create a notification for the teacher
        Notification.objects.create(
            recipient=teacher,
            message=f'{instance.student.user.username} has enrolled in your course "{instance.course.title}".'
        )