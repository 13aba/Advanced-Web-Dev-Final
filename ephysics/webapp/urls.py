
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import *
from . import views 

#Router for my projects api
router = DefaultRouter()
router.register(r'appusers', AppUserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'post', PostViewSet)
router.register(r'status', StatusViewSet)
router.register(r'enrollment', EnrollmentViewSet)
router.register(r'deadline', DeadlineViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'blockedstudents', BlockedStudentViewSet)
router.register(r'notification', NotificationViewSet)

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
    path('notifications/mark_notifications_read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('notifications/get_notifications/', views.get_notifications, name='get_notifications'),
    path('chat_room/<int:pk>/', views.chat_room, name='chat_room'),
    path('api/', include(router.urls)),
    path('api/appuser/<int:id>/', SingleAppUserAPIView.as_view(), name='single-user-api'),
    path('api/course/<int:id>/', SingleCourseAPIView.as_view(), name='single-course-api'),
    path('api/post/<int:id>/', SinglePostAPIView.as_view(), name='single-post-api'),
    path('api/enrollment/<int:id>/', SingleEnrollmentAPIView.as_view(), name='single-enrollment-api'),
    path('api/deadline/<int:id>/', SingleDeadlineAPIView.as_view(), name='single-deadline-api'),
    path('api/status/<int:id>/', SingleStatusAPIView.as_view(), name='single-status-api'),
    path('api/feedback/<int:id>/', SingleFeedbackAPIView.as_view(), name='single-feedback-api'),
    path('api/blockedstudent/<int:id>/', SingleBlockedStudentAPIView.as_view(), name='single-blockedstudent-api'),
    path('api/notification/<int:id>/', SingleNotificationAPIView.as_view(), name='single-notification-api'),
]