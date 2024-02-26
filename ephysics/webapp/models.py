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


# Create your models here.
