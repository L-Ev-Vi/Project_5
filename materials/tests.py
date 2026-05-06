from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson


class LessonAPITestCase(APITestCase):
    """Тесты 'уроки'."""

    def setUp(self):
        self.user = User.objects.create(email="jon@world.com", password="123")
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(title="Test", description="Text test", author=self.user)
        self.moderators = Group.objects.create(name="Модераторы")

    def test_create(self):
        """Тестирование создания урока."""

        url = reverse("materials:lesson-create")

        data = {"title": "Test1", "description": "Text test1", "video": "https://www.youtube.com/watch?v=P6QHswl2PqE"}
        error_data = {}
        error_video = {"title": "Test2", "description": "Text test2", "video": "https://www.rutube.ru?v=P6QHswl2PqE"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()["title"], data.get("title"))

        response = self.client.post(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, error_video)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json()["non_field_errors"], ["Ссылка на видео материал должен вести только на хостинг YouTube!"]
        )

        self.user.groups.add(self.moderators)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        """Тестирование получения списка уроков."""

        url = reverse("materials:lessons")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json().get("results")), 1)

        self.user.groups.add(self.moderators)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        """Тестирование получения урока."""

        url = reverse("materials:lesson-retrieve", args=[self.lesson.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["title"], self.lesson.title)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.groups.add(self.moderators)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        """Тестирование изменение урока."""

        url = reverse("materials:lesson-update", args=[self.lesson.pk])

        data = {"title": "Test3", "description": "Text test3"}
        error_data = {}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["title"], data.get("title"))

        response = self.client.patch(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.groups.add(self.moderators)
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.groups.add(self.moderators)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        """Тестирование удаление урока."""

        url = reverse("materials:lesson-destroy", args=[self.lesson.pk])

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.groups.add(self.moderators)
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)


class CourseAPITestCase(APITestCase):
    """Тесты 'курсы'."""

    def setUp(self):
        self.user = User.objects.create(email="jon@world.com", password="123")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test", description="Text test", author=self.user)
        self.moderators = Group.objects.create(name="Модераторы")

    def test_create(self):
        """Тестирование создания курса."""

        url = reverse("materials:course-list")

        data = {"title": "Test1", "description": "Text test1"}
        error_data = {}
        body = {
            "id": 2,
            "title": "Test1",
            "picture": None,
            "description": "Text test1",
            "author": 1,
            "lesson": [],
            "price": "0.00",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(), body)

        response = self.client.post(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.groups.add(self.moderators)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        """Тестирование получения списка курсов."""

        url = reverse("materials:course-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json().get("results")), 1)

        self.assertEqual(response.json().get("count"), 1)

        self.user.groups.add(self.moderators)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        """Тестирование получения курса."""

        url = reverse("materials:course-detail", args=[self.course.pk])
        body = {
            "id": 5,
            "title": "Test",
            "lessons": 0,
            "picture": None,
            "description": "Text test",
            "author": 5,
            "lesson": [],
            "subscriptions": False,
            "price": "0.00",
        }

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), body)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.groups.add(self.moderators)
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        """Тестирование изменение курса."""

        url = reverse("materials:course-detail", args=[self.course.pk])

        data = {"title": "Test3", "description": "Text test3"}
        error_data = {}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["title"], data.get("title"))

        response = self.client.patch(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.groups.add(self.moderators)
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.groups.add(self.moderators)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        """Тестирование удаление курса."""

        url = reverse("materials:course-detail", args=[self.course.pk])

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.groups.add(self.moderators)
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.all().count(), 0)
