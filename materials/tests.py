from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import CustomUser


class TestLesson(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test1@email.ru", password="test_password", username="test"
        )

        self.course_1 = Course.objects.create(name="test_course_1", owner=self.user)
        self.course_2 = Course.objects.create(name="test_course_2", owner=self.user)

        self.lesson_1 = Lesson.objects.create(
            name="test_lesson_1", course=self.course_1, owner=self.user
        )
        self.lesson_2 = Lesson.objects.create(
            name="test_lesson_2", course=self.course_2, owner=self.user
        )

        self.lessons_list_url = "/materials/lessons/"
        self.lesson_create_url = "/materials/lesson/create/"
        self.lesson_update_url = f"/materials/lesson/{self.lesson_1.pk}/update/"
        self.lesson_retrieve_url = f"/materials/lesson/{self.lesson_1.pk}/detail/"
        self.lesson_delete_url = f"/materials/lesson/{self.lesson_1.pk}/delete/"

        self.valid_data = {
            "name": "Новый Урок 3",
            "course": self.course_1.pk,
            "link_to_the_video": "https://www.youtube.com/watch?v=validID",
        }
        self.updated_data = {
            "name": "updated_item",
            "course": self.course_1.pk,
            "link_to_the_video": "https://www.youtube.com/watch?v=UPDATED_VIDEO_ID",
        }

    def test_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lessons_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.lesson_create_url, self.valid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            self.lesson_update_url, self.updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson_1.refresh_from_db()

    def test_retrieve(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.lesson_retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
