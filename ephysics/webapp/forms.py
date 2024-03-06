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

class DeadlineForm(forms.Form):
    title = forms.CharField(label='Task', widget=forms.TextInput(attrs={'placeholder': 'Deadline task', 'style': 'width: 90%; height: 30px; font-size: 20px;', 'class': 'form-control'}))
    due_date = forms.DateField(label='Due by:', widget=forms.SelectDateWidget(attrs={'style': 'width: 90%; height: 30px; font-size: 15px; padding-top: 0px; margin-bottom: 2px;', 'class': 'form-control'}))

class PostForm(forms.ModelForm):

    class Meta : 
        model = Post
        fields = ('title', 'content','image', 'file')

class FeedbackForm(forms.ModelForm):

    SCORE_CHOICES = (
        ('1', 'Highly Not Recommended'),
        ('2', 'Not Recommended'),
        ('3', 'Neutral'),
        ('4', 'Recommended'),
        ('5', 'Highly Recommended'),
    )

    score = forms.ChoiceField(choices=SCORE_CHOICES, initial='3', widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 90%;'}))

    class Meta : 
        model = Feedback
        fields = ('score', 'content')

        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Feedback for the course', 'style': 'width: 90%; resize: None; height: 70px;', 'class': 'form-control'})
        }