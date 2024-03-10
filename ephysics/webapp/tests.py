from django.test import override_settings, TestCase
from django.conf import settings

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .factories import *


#Passing test for getting single user data using 'single-user-api'
#Overriding our middleware since the middleware redirects everything to login page if user is not authenticated
#even if its from our test
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class AppUserAPITests(APITestCase):
    def setUp(self):
        self.user = AppUserFactory()

    def test_get_appuser(self):
        url = reverse('single-user-api', kwargs={'id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)

#Passing test for getting single course data using 'single-course-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class CourseAPITests(APITestCase):
    def setUp(self):
        self.course = CourseFactory()

    def test_get_course(self):
        url = reverse('single-course-api', kwargs={'id': self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)

#Passing test for getting single enrollment data using 'single-enrollment-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class EnrollmentAPITests(APITestCase):
    def setUp(self):
        self.enrollment = EnrollmentFactory()

    def test_get_enrollment(self):
        url = reverse('single-enrollment-api', kwargs={'id': self.enrollment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('course', response.data)
        self.assertIn('student', response.data)

#Passing test for getting single feedback data using 'single-feedback-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class FeedbackAPITests(APITestCase):
    def setUp(self):
        self.feedback = FeedbackFactory()

    def test_get_feedback(self):
        url = reverse('single-feedback-api', kwargs={'id': self.feedback.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('content', response.data)
        self.assertEqual(response.data['score'], self.feedback.score)

#Passing test for getting single post data using 'single-post-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class PostAPITests(APITestCase):
    def setUp(self):
        self.post = PostFactory()

    def test_get_post(self):
        url = reverse('single-post-api', kwargs={'id': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

#Passing test for getting single status data using 'single-status-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class StatusAPITests(APITestCase):
    def setUp(self):
        self.status = StatusFactory()

    def test_get_status(self):
        url = reverse('single-status-api', kwargs={'id': self.status.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('content', response.data)

#Passing test for getting single deadline data using 'single-deadline-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class DeadlineAPITests(APITestCase):
    def setUp(self):
        self.deadline = DeadlineFactory()

    def test_get_deadline(self):
        url = reverse('single-deadline-api', kwargs={'id': self.deadline.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data)

#Passing test for getting single feedback data using 'single-feedback-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class FeedbackAPITests(APITestCase):
    def setUp(self):
        self.feedback = FeedbackFactory()

    def test_get_feedback(self):
        url = reverse('single-feedback-api', kwargs={'id': self.feedback.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('score', response.data)

#Passing test for getting single blockedstudent data using 'single-blockedstudent-api'
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class BlockedStudentAPITests(APITestCase):
    def setUp(self):
        self.blocked_student = BlockedStudentFactory()

    def test_get_blocked_student(self):
        url = reverse('single-blockedstudent-api', kwargs={'id': self.blocked_student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('teacher', response.data)

#Failing test for getting user data who does not exist
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class AppUserAPIErrorTests(APITestCase):
    def test_get_nonexistent_appuser(self):
        url = reverse('single-user-api', kwargs={'id': 9999})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class CourseAPIErrorTests(APITestCase):
    def setUp(self):

        self.user = AppUserFactory()

    #Failing test for getting course data who does not exist
    def test_get_nonexistent_course(self):
        url = reverse('single-course-api', kwargs={'id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #Failing test for creating course while unauthorizes
    def test_create_course_unauthorized(self):
        url = reverse('course-list') 
        data = {'title': 'New Course', 'description': 'A new course.', 'teacher': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class EnrollmentAPIErrorTests(APITestCase):
    def test_get_nonexistent_enrollment(self):
        url = reverse('single-enrollment-api', kwargs={'id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #Failing test for creating enrollment with course that does not exist
    def test_create_enrollment_with_invalid_course(self):
        student = AppUserFactory()
        url = reverse('enrollment-list')  
        data = {'student': student.id, 'course': 9999}  
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class FeedbackAPIErrorTests(APITestCase):
    
    #Failing test for getting feedback data that does not exist
    def test_get_nonexistent_feedback(self):
        url = reverse('single-feedback-api', kwargs={'id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    #Failing test for creating feedback with invalid score
    def test_create_feedback_with_invalid_score(self):
        course = CourseFactory()
        student = AppUserFactory()
        url = reverse('feedback-list') 
        data = {'course': course.id, 'student': student.id, 'score': 'invalid', 'content': 'Great course!'}  
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#Not bypassing middleware thus should redirect to login page
class PostAPITestsFailing(APITestCase):
    
    #Failing test for creating post while unauthorizes
    def test_get_post_unauthorized(self):
        post = PostFactory()
        url = reverse('single-post-api', kwargs={'id': post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


#Failing test for creating new status without any content message
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class StatusAPITestsFailing(APITestCase):
    def test_create_status_without_content(self):
        user = AppUserFactory()
        self.client.force_authenticate(user=user.user)
        url = reverse('status-list')  
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#Failing test for creating deadline with bad date data 
@override_settings(MIDDLEWARE=[mw for mw in settings.MIDDLEWARE if mw != 'webapp.middleware.LoginMiddleware'])
class DeadlineAPITestsFailing(APITestCase):
    def test_create_deadline_bad_date(self):
        course = CourseFactory()
        self.client.force_authenticate(user=course.teacher.user)
        url = reverse('deadline-list')  
        data = {
            'course': course.id,
            'title': 'Bad Deadline',
            'due_date': '2000-2020-2020'  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





