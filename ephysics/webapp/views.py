from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from datetime import date


def register(request):


    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            
            #Check if form is not null and update the profile with the given data
            if 'first_name' in user_form.cleaned_data:
                profile.first_name = user_form.cleaned_data['first_name']
            if 'last_name' in user_form.cleaned_data:
                profile.last_name = user_form.cleaned_data['last_name']
            if 'age' in user_form.cleaned_data:
                profile.age = user_form.cleaned_data['age']
            if 'is_student' in user_form.cleaned_data:
                profile.is_student = user_form.cleaned_data['is_student']

            profile.save()
            
            #Send user to login page if registered successfully
            messages.success(request, 'You have been registered successfully. Please log in.')
            return redirect('/login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form' : user_form,
        'profile_form': profile_form,
    }

    return render(request, 'register.html', context)


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            
            login(request, user)
            return redirect('/')
    
        else:
            messages.error(request, "Invalid login details supplied.")
            return redirect('/login')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

def index(request):

    #Get the user profile from request
    user = request.user.appuser
    #Check if the user is student or teacher
    if user.is_student:
        #Get the enrolled courses for students
        try:
            courses = Enrollment.objects.values_list("course").filter(student = user)
        except Exception:
            courses = None
        context = {
            'courses': courses
        }
        #Display student home page
        return render(request, 'student_index.html', context)
    else:
        #Get the courses created by the teacher
        try:
            courses = Course.objects.filter(teacher = user)
        except Exception:
            courses = None
        context = {
            'courses' : courses
        } 
        #Display teacher home page
        return render(request, 'teacher_index.html', context)  

    


def courses(request):

    courses = Course.objects.all()
    context = {
        'courses': courses
    }

    return render(request, 'courses.html', context)


def course(request, pk):

    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course.html', context)

def profile(request):

    user = request.user
    profile = user.appuser 

    if request.method == 'POST':
        
        profile_form = UserProfileForm(data = request.POST, instance=profile)
        
        if profile_form.is_valid():
            #Save profile if form is valid and successful message
            profile.save()
        else:
            #Error message if profile form is not valid  
            messages.error(request, profile_form.errors)
            #Return user to profile section
            return redirect('/profile') 

        #Set new password if its changed
        #This section has been referenced and modified from 
        # https://stackoverflow.com/questions/30821795/django-user-logged-out-after-password-change
        if 'new_password' in request.POST:
            password_form = PasswordChangeForm(data=request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                new_password = password_form.cleaned_data['new_password']
                if new_password:
                    #Check if old password match 
                    user = authenticate(request, username=request.user.username, password=old_password)
                    if user is not None:
                        try:
                            user.set_password(new_password)
                            user.save()
                        except Exception:
                            messages.error(request, "Problem changing password")
                            return redirect('/profile')
                        #Update session authorization so users dont get redirected to login page from our middleware
                        update_session_auth_hash(request, user) 
                        messages.success(request, 'Password updated successfully')
                        return redirect('/profile')
                    else:
                        # No backend authenticated the credentials
                        messages.error(request, 'Old password is not correct')
                        return redirect('/profile')
            else:
                #Send error message if password form is valid
                for error in password_form.errors:
                    messages.error(request, password_form.errors[error]) 
                return redirect('/profile')

        #If everythins correct and valid push succesful message and redirect user to profile page
        messages.success(request, 'Profile updated succesfully')
        return redirect('/profile')

    else:
        password_form = PasswordChangeForm()
        profile_form = UserProfileForm(instance=profile)

    context = {
        'password_form': password_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)


def create_course(request):

    user = request.user.appuser

    if request.method == 'POST':
        course_form = CourseForm(data = request.POST)
        if course_form.is_valid():
            #Create new course from our the form and date
            course = Course(title = course_form.cleaned_data['title'],
                            description = course_form.cleaned_data['description'],
                            created = date.today(),
                            modified = date.today(),
                            teacher = user)
            #Save the course
            course.save()
            #Return success message and redirect back to home page
            messages.success(request, 'Course created succesfully')
            return redirect('/')
    else:
        course_form = CourseForm()
    
    context = {
        'course_form': course_form
    }
    return render(request, 'create_course.html', context)

def delete_course(request, pk):

    user = request.user.appuser

    if request.method == 'POST':
        course = Course.objects.get(id=pk)

        #Check if teacher requesting deletion is the teacher that created the course
        if user == course.teacher:
            course.delete()
            #Return success message and redirect back to home page
            messages.success(request, 'Course deleted succesfully')
            return redirect('/')
        else:
            #Return error message and redirect back to home page
            messages.error(request, 'Something wrong with the request please check the URL and try again')
            return redirect('/')