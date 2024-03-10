import factory
from django.contrib.auth.models import User
from .models import AppUser, Course, Post, Enrollment, Status, Deadline, Feedback, BlockedStudent, Notification
from factory.django import DjangoModelFactory
import datetime

#Create factories that produce fake test data for each models
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.LazyAttribute(lambda obj: "%s@example.com" % obj.username)

class AppUserFactory(DjangoModelFactory):
    class Meta:
        model = AppUser

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    age = factory.Faker('pyint', min_value=18, max_value=100)
    is_student = factory.Faker('boolean')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Sequence(lambda n: "Course %d" % n)
    description = factory.Faker('text')
    created = factory.LazyFunction(datetime.date.today)
    modified = factory.LazyFunction(datetime.date.today)
    teacher = factory.SubFactory(AppUserFactory)

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker('sentence')
    content = factory.Faker('text')
    created = factory.LazyFunction(datetime.date.today)

class EnrollmentFactory(DjangoModelFactory):
    class Meta:
        model = Enrollment

    student = factory.SubFactory(AppUserFactory)
    course = factory.SubFactory(CourseFactory)
    enrolled_at = factory.LazyFunction(datetime.date.today)

class StatusFactory(DjangoModelFactory):
    class Meta:
        model = Status

    user = factory.SubFactory(AppUserFactory)
    content = factory.Faker('text')
    created_at = factory.LazyFunction(datetime.date.today)

class DeadlineFactory(DjangoModelFactory):
    class Meta:
        model = Deadline

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker('sentence')
    due_date = factory.LazyFunction(datetime.date.today)

class FeedbackFactory(DjangoModelFactory):
    class Meta:
        model = Feedback

    course = factory.SubFactory(CourseFactory)
    student = factory.SubFactory(AppUserFactory)
    date = factory.LazyFunction(datetime.date.today)
    score = factory.Iterator(['1', '2', '3', '4', '5'])
    content = factory.Faker('text')

class BlockedStudentFactory(DjangoModelFactory):
    class Meta:
        model = BlockedStudent

    teacher = factory.SubFactory(AppUserFactory, is_student=False)
    student = factory.SubFactory(AppUserFactory, is_student=True)