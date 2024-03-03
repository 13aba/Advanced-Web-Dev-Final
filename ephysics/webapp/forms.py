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

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(required=False, label="Old Password", widget=forms.PasswordInput)
    new_password = forms.CharField(required=False, label="New Password", widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(required=False, label="Confirm New Password", widget=forms.PasswordInput)

    def clean(self):
        #Clean the data
        cleaned_data = super().clean()
        new_password = cleaned_data["new_password"]
        confirm_new_password = cleaned_data["confirm_new_password"]
        #Check if user entered same password twice
        if new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")
        #Return cleaned data if form is valid
        return cleaned_data

class CourseForm(forms.Form):
    title = forms.CharField(label="Course Title")
    description = forms.CharField(label="Course Description", widget=forms.Textarea)

class StatusForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Update your status', 'style': 'width: 100%; resize: None; height: 100px;', 'class': 'form-control'}))