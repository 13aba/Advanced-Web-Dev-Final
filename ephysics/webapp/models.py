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
    image = models.ImageField(upload_to="images/", blank=True)
    icon = models.FileField(null=True, blank=True)

    def __unicode__ (self):
        return self.user.username

    def __str__ (self):
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
    image = models.ImageField(upload_to="images/", blank=True)
    file = models.FileField(upload_to="files/", blank=True)

class Enrollment(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateField(editable=False)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

class Status(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(editable=False)

    def __str__(self):
        return f"{self.user.user.username} added new status at {self.created_at}"

class Deadline(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    due_date = models.DateField(editable=False)

    def __str__(self):
        return f"{self.course.title} have deadline at {self.due_date}"

class FeedbackChoice:
    SCORE_CHOICES = (
        ('1', 'Highly Not Recommended'),
        ('2', 'Not Recommended'),
        ('3', 'Neutral'),
        ('4', 'Recommended'),
        ('5', 'Highly Recommended'),
    )

class Feedback(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateField(editable=False)
    score = models.CharField(max_length=1, choices = FeedbackChoice.SCORE_CHOICES)
    content = models.TextField()

    def __str__(self):
        return f"{self.course.title} have feedback from {self.student}"

    #Referenced from https://forum.djangoproject.com/t/django-get-foo-display-not-working-as-expected/23866/7
    @property
    def get_score_text(self):
        for i in FeedbackChoice.SCORE_CHOICES:
            if i[0] == self.score:
                return i[1]
        return self.score

class BlockedStudent(models.Model):
    teacher = models.ForeignKey(AppUser, related_name='blocked_students', on_delete=models.CASCADE)
    student = models.ForeignKey(AppUser, related_name='blocked_by_teachers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.user.username} blocked {self.student.user.username}"

class Notification(models.Model):
    recipient = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.user.username}: {self.message}"

