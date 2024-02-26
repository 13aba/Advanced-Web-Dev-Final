from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta : 
        model = AppUser
        fields = ('first_name', 'last_name', 'age', 'is_student')