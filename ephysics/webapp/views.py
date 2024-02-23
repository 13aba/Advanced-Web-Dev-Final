from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
            if 'firstName' in user_form.cleaned_data:
                profile.firstName = user_form.cleaned_data['firstName']
            if 'lastName' in user_form.cleaned_data:
                profile.lastName = user_form.cleaned_data['lastName']
            if 'age' in user_form.cleaned_data:
                profile.age = user_form.cleaned_data['age']

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

    return render(request, 'index.html')
