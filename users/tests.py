import datetime

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Payments, Subscriptions, User

from .models import Course, Lesson


class UserAPITestCase(APITestCase):
    """Тесты 'Пользователь'."""

    def setUp(self):
        self.user = {"email": "jon@world.com", "password": "123"}
        self.user2 = {"email": "tom@world.com", "password": "123"}
        self.moderators = Group.objects.create(name="Модераторы")

    def test_create(self):
        """Тестирование регистрация пользователя."""

        url = reverse("users:users-list")

        error_data = {}
        error_email = {"email": "jon.com", "password": "123"}

        response = self.client.post(url, self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(response.json()["email"], self.user.get("email"))

        response = self.client.post(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, error_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, self.user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.all().count(), 2)

        user = User.objects.get(pk=User.objects.all()[0].pk)
        user.groups.add(self.moderators)
        self.assertEqual(User.objects.get(pk=User.objects.all()[0].pk).groups.all()[0], self.moderators)

    def test_list(self):
        """Тестирование получения списка уроков."""

        url = reverse("users:users-list")
        user = User.objects.create(email="jon@world.com", password="123")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 1)

        self.assertEqual(response.json()[0]["email"], user.email)

    def test_retrieve(self):
        """Тестирование получения данных пользователя."""

        self.user = User.objects.create(email="jon@world.com", password="123")
        self.client.force_authenticate(self.user)

        url = reverse("users:users-detail", args=[self.user.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["email"], self.user.email)

        self.assertEqual(response.json().get("email"), self.user.email)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get("email"), self.user.email)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        """Тестирование редактирование пользователя."""

        self.user = User.objects.create(email="jon@world.com", password="123")
        self.client.force_authenticate(self.user)

        url = reverse("users:users-detail", args=[self.user.pk])

        data = {"city": "Инсар"}
        error_data = {}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["city"], data.get("city"))

        response = self.client.patch(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        """Тестирование удаление пользователя."""

        self.user = User.objects.create(email="jon@world.com", password="123")

        url = reverse("users:users-detail", args=[self.user.pk])

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(User.objects.all().count(), 2)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(User.objects.all().count(), 1)


class PaymentsAPITestCase(APITestCase):
    """Тесты 'Платёж'."""

    def setUp(self):
        self.user = User.objects.create(email="jon@world.com", password="123")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Course", description="Text test", author=self.user)
        self.lesson = Lesson.objects.create(title="Lesson", description="Text test", author=self.user)

    def test_create(self):
        """Тестирование создание платежа."""

        url = reverse("users:payments-create")

        data_course = {"course": self.course.pk, "title": self.course.title}
        data_lesson = {"lesson": self.lesson.pk, "title": self.lesson.title}
        error_data = {}
        error_amount = {"amount": ""}

        response = self.client.post(url, data_course)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Payments.objects.all().count(), 1)
        self.assertEqual(response.json()["amount"], "0.00")

        response = self.client.post(url, data_lesson)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Payments.objects.all().count(), 2)
        self.assertEqual(response.json()["amount"], "0.00")

        response = self.client.post(url, error_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, error_amount)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(user=None)
        response = self.client.post(url, data_course)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        """Тестирование получения списка платежей."""

        url = reverse("users:payments")

        self.payments_course = Payments.objects.create(user=self.user, course=self.course, amount=100, method="cash")
        self.payments_lesson = Payments.objects.create(
            user=self.user, lesson=self.lesson, amount=200, method="translation"
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Payments.objects.all().count(), 2)

        response = self.client.get(url + "?ordering=date")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 2)

        response = self.client.get(url + f"?course={self.course.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["course"], self.course.pk)

        response = self.client.get(url + f"?lesson={self.lesson.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["lesson"], self.lesson.pk)

        response = self.client.get(url + "?ordering=-date&method=cash")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["course"], self.course.pk)

        response = self.client.get(url + "?ordering=-date&method=translation")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["lesson"], self.lesson.pk)

        response = self.client.get(url + f"?ordering=-date&method=translation&course={self.course.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 0)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        """Тестирование получения платежа."""

        self.payments_course = Payments.objects.create(
            user=self.user,
            course=self.course,
            amount=100,
            method="cash",
            session={"id": "1", "payment_status": "paid", "url": "stripe"},
        )

        url = reverse("users:payments-retrieve", args=[self.payments_course.pk])

        body = {
            "id": 5,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "amount": "100.00",
            "method": "cash",
            "user": 19,
            "course": 9,
            "lesson": None,
            "session": {"id": "1", "payment_status": "paid", "url": "stripe"},
        }

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), body)

        user = User.objects.create(email="tom@world.com", password="123")
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionsAPITestCase(APITestCase):
    """Тесты 'Подписка'."""

    def setUp(self):
        self.user = User.objects.create(email="jon@world.com", password="123")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Course", description="Text test", author=self.user)

    def test_post(self):
        """Тестирование включения и отключения подписки"""

        url = reverse("users:subscriptions")
        url_course_detail = reverse("materials:course-detail", args=[self.course.pk])

        response = self.client.get(url_course_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(response.json()["subscriptions"])

        response = self.client.post(url, {"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "Подписка включена!"})
        self.assertTrue(Subscriptions.objects.get(user=self.user, course=self.course).subscription)

        response = self.client.post(url, {"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "Подписка отключена!"})
        self.assertFalse(Subscriptions.objects.get(user=self.user, course=self.course).subscription)
