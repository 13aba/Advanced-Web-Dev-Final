from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *
from .tasks import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from datetime import date
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#Decorator used for restircting students from some of our web application
def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        #If teacher direct to requested view function
        if not request.user.appuser.is_student:  
            return view_func(request, *args, **kwargs)
        #If student give error message and redirect back to home page
        else:
            #If anything wrong show error message and redirect back to last page
            messages.warning(request, 'You are not authorized for this function/page')
            #Send user back to the home page if requested course doesnot exist
            return redirect('/')
    return wrapper

#Used to display register page htmls and create new user if method is POST
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
        #Check if username and password match
        if user:
            #If credentials are correct login the user and redirect to home
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Invalid login details supplied.")
            return redirect('/login')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

def index(request):

    #Get the user profile from request
    user = request.user.appuser
    #Create form for posting status for both teacher and student
    status_form = StatusForm()
    #Check if the user is student or teacher
    if user.is_student:
        #Get the enrolled courses and status updates for students
        try:
            enrollments = Enrollment.objects.filter(student = user)
        except Exception:
            enrollments = None

        try:
            status = Status.objects.filter(user = user)
        except Exception:
            status = None
        
        try:
            deadlines = Deadline.objects.filter(course__enrollment__student=user, due_date__gte=date.today())
        except Exception:
            deadlines = None

        context = {
            'appuser': user,
            'enrollments': enrollments,
            'status': status,
            'status_form': status_form,
            'deadlines': deadlines
        }
        #Display student home page
        return render(request, 'student_index.html', context)
    else:
        #Get the courses created by the teacher and status updates
        try:
            courses = Course.objects.filter(teacher = user)
        except Exception:
            courses = None
        
        try:
            status = Status.objects.filter(user = user)
        except Exception:
            status = None

        context = {
            'appuser': user,
            'courses' : courses,
            'status': status,
            'status_form': status_form
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

    #Get the user profile from request
    user = request.user.appuser

    try: 
        course = Course.objects.get(id = pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

    #Check if user is already enrolled to the course 
    try:
        enrollment = Enrollment.objects.get(course = course, student = user)
        #If user is already enrolled send that information to frontend
        is_enrolled = True
        
    except:
        #If user is not enrolled
        is_enrolled = False 

    #Check if user is already submitted feedback
    try:
        course = Course.objects.get(id = pk)
        feedback = Feedback.objects.get(course = course, student = user)
        #If user is already enrolled send that information to frontend
        feedback_submitted = True
        
    except:
        #If user is not submitted feedback
        feedback_submitted = False

    #Get the enrolled students for the course
    try:
        enrollments = Enrollment.objects.filter(course = course)
    except Exception:
        enrollments = None
   
    #Get the enrolled students for the course
    try:
        feedbacks = Feedback.objects.all()
    except Exception:
        feedbacks = None

    #Get all posts and deadlines related to the course
    posts = Post.objects.filter(course = course)
    deadlines = Deadline.objects.filter(course = course)

    deadline_form = DeadlineForm()
    feedback_form = FeedbackForm()
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'deadline_form': deadline_form,
        'posts': posts,
        'deadlines': deadlines,
        'enrollments': enrollments,
        'feedback_form': feedback_form,
        'feedbacks': feedbacks,
        'feedback_submitted': feedback_submitted
    }
    return render(request, 'course.html', context)

def profile(request):

    user = request.user
    profile = user.appuser 

    if request.method == 'POST':
        
        profile_form = UserProfileForm(request.POST,  request.FILES, instance=profile)
        
        if profile_form.is_valid():
            #Save profile if form is valid and successful message
            profile.save()
            
        else:
            #Error message if profile form is not valid  
            messages.warning(request, profile_form.errors)
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
                            messages.warning(request, "Problem changing password")
                            return redirect('/profile')
                        #Update session authorization so users dont get redirected to login page from our middleware
                        update_session_auth_hash(request, user) 
                        messages.success(request, 'Password updated successfully')
                        return redirect('/profile')
                    else:
                        # No backend authenticated the credentials
                        messages.warning(request, 'Old password is not correct')
                        return redirect('/profile')
            else:
                #Send error message if password form is valid
                for error in password_form.errors:
                    messages.warning(request, password_form.errors[error]) 
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
        'profile': profile
    }
    return render(request, 'profile.html', context)


@teacher_required
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
            #Return error message and redirect back to home page
            messages.warning(request, 'Unable to create course succesfully')
            return redirect('/')
    else:
        course_form = CourseForm()
    
    context = {
        'course_form': course_form
    }
    return render(request, 'create_course.html', context)

def create_status(request):

    user = request.user.appuser

    if request.method == 'POST':
        status_form = StatusForm(data = request.POST)
        if status_form.is_valid():
            status = Status(
                user = user,
                content = status_form.cleaned_data['content'],
                created_at = date.today()
            )
            #Save the course
            status.save()
            #Return success message and redirect back to home page
            messages.success(request, 'Status created succesfully')
            return redirect('/')
           
        else:
            #Return error message and redirect back to home page
            messages.warning(request, 'Unable to create status succesfully')
            return redirect('/')
    else:
        #Return error message and redirect back to home page
        messages.warning(request, 'Unable to create status succesfully')
        return redirect('/')
    
@teacher_required
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
            messages.warning(request, 'Something wrong with the request please check the URL and try again')
            return redirect('/')

def enroll_course(request, pk):

    user = request.user.appuser
    #Check if user request using POST and if user is student 
    #(We dont want teachers to be able to enroll into class. Teacher can create another student account for that purposes)
    if request.method == 'POST' and user.is_student:
        try:
            course = Course.objects.get(id = pk)
        except Exception:
            messages.warning(request, 'Could not find the course, try again later')
            return redirect('/')

        #Check if user is blocked by the teacher
        try: 
            blocked = BlockedStudent.objects.get(teacher = course.teacher, student = user)
            #If student show up on blockedstudent
            messages.warning(request, 'The teacher of this course blocked you. Unable to enroll')
            #Send user back to the home page if requested course doesnot exist
            return redirect('/')
        except Exception:
            #Just pass if student does not show up on blocked list
            pass


        #Create new enrollment
        enrollment = Enrollment(student = user,
                                course = course,
                                enrolled_at = date.today()
        )
        #Save the new enrollment
        enrollment.save()
        #Return success message and redirect back to home page
        messages.success(request, f'Enrolled successfully to course {course.title}')

        return redirect(f'/course/{pk}')
    else:
        #If anything wrong show error message and redirect back to last page
        messages.warning(request, 'Something wrong with the enroll request try again')
        #Send user back to the home page if requested course doesnot exist
        return redirect('/')
        
def leave_course(request, pk):

    user = request.user.appuser
    #Check if user request using POST and if user is student 
    #(We dont want teachers to be able to enroll and leave into class. Teacher can create another student account for that purposes)
    if request.method == 'POST' and user.is_student:
        try:
            course = Course.objects.get(id = pk)
        except Exception:
            messages.warning(request, 'Could not find the course, try again later')
            #Send user back to the home page if requested course doesnot exist
            #Referenced from https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request
            return redirect('/')
        #Find the enrollment object
        enrollment = Enrollment.objects.get(course = course, student = user)
        #Delete the enrollment object
        enrollment.delete()
        #Return success message and redirect back to course page
        messages.success(request, f'Left course {course.title} successfully')
        return redirect(f'/course/{pk}')
    else:
        #If anything wrong show error message and redirect back to last page
        messages.warning(request, 'Something wrong with the enroll request try again')
        #Send user back to the home page if requested course doesnot exist
        return redirect('/')

@teacher_required
def create_deadline(request, pk):

    #Get the user profile from request
    user = request.user.appuser

    #Check if user is course exist to create new deadline
    try:
        course = Course.objects.get(id = pk)
    except:
        #If course does not exist send user back after sending error message
        messages.warning(request, 'Something wrong with the enroll request try again')
        #Send user back to the home page if requested course doesnot exist
        return redirect('/')

    if request.method == 'POST':
        deadline_form = DeadlineForm(data = request.POST)
        if deadline_form.is_valid():
            deadline = Deadline(
                course = course,
                title = deadline_form.cleaned_data['title'],
                due_date = deadline_form.cleaned_data['due_date'],
            )
            #Save the deadline
            deadline.save()
            #Return success message and redirect back to home page
            messages.success(request, 'Deadline created succesfully')
            return redirect('/')
           
        else:
            #Return error message and redirect back to home page
            messages.warning(request, 'Unable to create status succesfully')
            return redirect('/')
    else:
        #Return error message and redirect back to home page
        messages.warning(request, 'Unable to create deadline, please try again')
        return redirect('/')

@teacher_required
def delete_deadline(request, pk):

    user = request.user.appuser

    try:
        deadline = Deadline.objects.get(id=pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

    #Check if teacher requesting deletion is the teacher that created the course
    if user == deadline.course.teacher:
        deadline.delete()
        #Return success message and redirect back to home page
        messages.success(request, 'Deadline deleted succesfully')
        return redirect('/')
    else:
        #Return error message and redirect back to home page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

@teacher_required
def create_post(request, pk):
    
    user = request.user.appuser
    #Check if requested course exist
    try:
        course = Course.objects.get(id = pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

    if request.method == 'POST':
        #Check if user is creater of the course
        if user == course.teacher: 
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                # Set the course for the post
                post.course = course
                post.created = date.today()
                post.save()
                # Return a success message and redirect back to course page
                messages.success(request, 'Post created successfully.')
                return redirect(f'/course/{pk}')
        else:
            #Return error message and redirect back to previous page
            messages.warning(request, 'Not authorized reqeust, please try again later!')
            return redirect('/')
            
    else:
        # If it's a GET request, create a blank form
        post_form = PostForm()
    
    context = {
        'course': course,
        'post_form': post_form
    }
    # Render the template with the form
    return render(request, 'create_post.html', context)

@teacher_required
def delete_post(request, pk):

    user = request.user.appuser

    try:
        post = Post.objects.get(id=pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

    #Check if teacher requesting deletion is the teacher that created the course
    if user == post.course.teacher:
        post.delete()
        #Return success message and redirect back to home page
        messages.success(request, 'Post deleted succesfully')
        return redirect('/')
    else:
        #Return error message and redirect back to home page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

def create_feedback(request, pk):
    
    user = request.user.appuser
    #Check if requested course exist
    try:
        course = Course.objects.get(id = pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            # Set the course and student for the feedback
            feedback.course = course
            feedback.student = user
            feedback.date= date.today()
            feedback.save()
            # Return a success message and redirect back to course page
            messages.success(request, 'Feedback submitted successfully.')
            return redirect(f'/course/{pk}')
        else:
             #If form is invalid
            messages.warning(request, 'Something wrong with the request form please check the URL and try again.')
            return redirect('/')

            
    else: 
        #If user tries to access this function outside of POST method
        messages.warning(request, 'Something wrong with the request please check the URL and try again.')
        return redirect('/')

@teacher_required
def block_student(request, pk):

    user = request.user.appuser

    #Check if requested student exist
    try:
        student = AppUser.objects.get(id = pk)
    except:
        #If student does not exist
        messages.warning(request, 'Something wrong with the request please check the URL and try again.')
        return redirect('/')
    
    if request.method == 'POST':
        #Create new blockedstudent object and save it
        blocked = BlockedStudent(
                                student = student,
                                teacher = user
        )
        blocked.save()
        #Remove students from every course our teacher has
        #Get every course created by the user
        user_courses = Course.objects.filter(teacher = user)
        #Get every enrollment from the blocked student to the teacher
        tbdeleted_enrollments = Enrollment.objects.filter(course__in = user_courses, student = student)
        #Delete the enrollments
        tbdeleted_enrollments.delete()
        #return success message
        messages.success(request, 'Student blocked successfully!')
        return redirect('/')

    else:
        messages.warning(request, 'Something wrong with the request please check the URL and try again.')
        return redirect('/')

@teacher_required
def unblock_student(request, pk):

    user = request.user.appuser

    #Check if student exist
    try:
        student = AppUser.objects.get(id = pk)
    except: 
        messages.warning(request, 'Something wrong with the request please check the URL and try again.')
        return redirect('/')
    #Make sure student is blocked
    try: 
        block = BlockedStudent.objects.get(teacher = user, student= student)
        #Delete that block if exist
        block.delete()
        #Send success message
        messages.success(request, 'Student unblocked successfully!')
        return redirect('/')
    except:
        messages.warning(request, 'Something wrong with the request please check the URL and try again.')
        return redirect('/')

def users(request):
    
    #Get all the users
    users = AppUser.objects.all()
    context = {
        'users': users
    }
    #Render html with all users data
    return render(request, 'users.html', context)

def user(request, pk):
    #Check if the request user exist
    user = request.user.appuser
    try:
        user_profile = AppUser.objects.get(id = pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')
    #Check if user is blocked
    try:
        blocked = BlockedStudent.objects.get(teacher=user, student=user_profile)
    except Exception as error:
        print(error)
        blocked = None
    #Get all status for the user
    statuses = Status.objects.filter(user = user_profile)
    context = {
        'user_profile': user_profile,
        'statuses': statuses,
        'blocked': blocked
    }
    
    #Render the user profile using the data from our query
    return render(request, 'user.html', context)  


#Logic to render chat room html
def chat_room(request, pk):
    current_user_id = request.user.appuser.id
    other_user_id = pk
    #Room name has to be same when two user connect to one chatroom. Implemented new function that
    #gives same room_name whether user is the number 1 or number 2
    room_name = generate_room_name(current_user_id, other_user_id)
    
    #get other users information
    try:
        other_user = AppUser.objects.get(id = pk)
    except:
        #Return error message and redirect back to previous page
        messages.warning(request, 'Something wrong with the request please check the URL and try again')
        return redirect('/')

    context = {
        'room_name': room_name,
        'other_user': other_user
    }
    return render(request, 'chat.html', context)

#Function create unified name for two users trying to chat with each other
def generate_room_name(user1_id, user2_id):
    #Generate a unique room name based on user IDs by sorting them and andding it to '_'.
    return "_".join(sorted([str(user1_id), str(user2_id)]))


#Function created to handle AJAX scripts for updating and polling notification from backend
@require_POST
@csrf_exempt 
def mark_notifications_read(request):
    Notification.objects.filter(recipient=request.user.appuser, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user.appuser, is_read=False).values('id', 'message')
    return JsonResponse(list(notifications), safe=False)
