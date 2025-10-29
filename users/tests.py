from django.test import TestCase
from materials.models import Course
from users.models import Subscription
from users.models import CustomUser


class SubscriptionModelTests(TestCase):

    def setUp(self):
        self.course_owner = CustomUser.objects.create_user(
            email="owner@example.com",
            password="test_password",
            username="course_owner"
        )

        self.subscriber = CustomUser.objects.create_user(
            email="subscriber@example.com",
            password="test_password",
            username="subscriber"
        )

        self.course = Course.objects.create(
            name="Test Course",
            owner=self.course_owner
        )

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(
            user=self.subscriber,
            course=self.course
        )

        self.assertTrue(Subscription.objects.exists())
        self.assertEqual(Subscription.objects.count(), 1)

        self.assertEqual(subscription.user, self.subscriber)
        self.assertEqual(subscription.course, self.course)
        self.assertIn(subscription, self.course.follower_course.all())
        self.assertIn(subscription, self.subscriber.follower.all())

    def test_subscription_deletion(self):
        subscription = Subscription.objects.create(
            user=self.subscriber,
            course=self.course
        )
        self.assertEqual(Subscription.objects.count(), 1)

        subscription.delete()
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertFalse(Subscription.objects.exists())

    def test_null_and_blank_fields(self):
        subscription_null = Subscription.objects.create(user=None, course=None)

        self.assertTrue(Subscription.objects.filter(pk=subscription_null.pk).exists())
        self.assertIsNone(subscription_null.user)
        self.assertIsNone(subscription_null.course)