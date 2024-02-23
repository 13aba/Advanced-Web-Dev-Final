from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    #This section handles username, password, and email
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    #This section handles user real name and age
    firstName = models.CharField(max_length = 20)
    lastName = models.CharField(max_length = 20)
    age = models.IntegerField()

    def __unicode__ (self):
        return self.user.username


# Create your models here.
