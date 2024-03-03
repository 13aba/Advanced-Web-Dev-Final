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
]