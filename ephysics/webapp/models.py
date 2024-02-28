from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    #This section handles username, password, and email
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    #This section handles user real name and age
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    age = models.IntegerField()
    is_student = models.BooleanField()

    def __unicode__ (self):
        return self.user.username

#Table for courses

class Course(models.Model):
    
    title = models.CharField(max_length=20)
    description = models.TextField()
    created = models.DateField(editable=False)
    modified = models.DateField()
    teacher = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__ (self):
        return self.title


class Post(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    created = models.DateField(editable=False)

class Enrollment(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateField(editable=False)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"