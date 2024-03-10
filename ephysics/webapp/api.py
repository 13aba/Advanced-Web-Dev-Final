from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404


#API routes for each models to see ALL user data
class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class DeadlineViewSet(viewsets.ModelViewSet):
    queryset = Deadline.objects.all()
    serializer_class = DeadlineSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class BlockedStudentViewSet(viewsets.ModelViewSet):
    queryset = BlockedStudent.objects.all()
    serializer_class = BlockedStudentSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


#API routes for each models to see INDIVIDUAL user data
class SingleAppUserAPIView(APIView):

    def get(self, request, id, format=None):
        user = get_object_or_404(AppUser, id=id)
        serializer = AppUserSerializer(user)
        return Response(serializer.data)

class SingleCourseAPIView(APIView):

    def get(self, request, id, format=None):
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

class SinglePostAPIView(APIView):

    def get(self, request, id, format=None):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

class SingleEnrollmentAPIView(APIView):

    def get(self, request, id, format=None):
        enrollment = get_object_or_404(Enrollment, id=id)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

class SingleStatusAPIView(APIView):

    def get(self, request, id, format=None):
        status = get_object_or_404(Status, id=id)
        serializer = StatusSerializer(status)
        return Response(serializer.data)

class SingleDeadlineAPIView(APIView):

    def get(self, request, id, format=None):
        deadline = get_object_or_404(Deadline, id=id)
        serializer = DeadlineSerializer(deadline)
        return Response(serializer.data)

class SingleFeedbackAPIView(APIView):

    def get(self, request, id, format=None):
        feedback = get_object_or_404(Feedback, id=id)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

class SingleBlockedStudentAPIView(APIView):

    def get(self, request, id, format=None):
        blockedstudent = get_object_or_404(BlockedStudent, id=id)
        serializer = BlockedStudentSerializer(blockedstudent)
        return Response(serializer.data)

class SingleNotificationAPIView(APIView):

    def get(self, request, id, format=None):
        notification = get_object_or_404(Notification, id=id)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
