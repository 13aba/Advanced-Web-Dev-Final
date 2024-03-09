from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:pk>', views.course, name='course'),
    path('create_course/', views.create_course, name='create_course'),
    path('create_status/', views.create_status, name='create_status'),
    path('delete_course/<int:pk>', views.delete_course, name='delete_course'),
    path('enroll_course/<int:pk>', views.enroll_course, name='enroll_course'),
    path('leave_course/<int:pk>', views.leave_course, name='leave_course'),
    path('create_deadline/<int:pk>', views.create_deadline, name='create_deadline'),
    path('delete_deadline/<int:pk>', views.delete_deadline, name='delete_deadline'),
    path('create_post/<int:pk>', views.create_post, name='create_post'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('create_feedback/<int:pk>', views.create_feedback, name='create_feedback'),
    path('block_student/<int:pk>', views.block_student, name='block_student'),
    path('unblock_student/<int:pk>', views.unblock_student, name='unblock_student'),
    path('users/', views.users, name='users'),
    path('user/<int:pk>', views.user, name='user'),
]