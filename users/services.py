from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from stripe import StripeClient, error
from rest_framework import exceptions
from .models import User

from config import settings
from .tasks import blocking

from datetime import timedelta

client = StripeClient(settings.STRIPE_API_KEY)


class StripePayments:
    """Класс для работы с платежами через сервис 'stripe'."""

    @staticmethod
    def online_payment(name_product, description, amount):
        """Создание сессии платежа"""

        try:
            product = client.v1.products.create(
                {
                    "name": name_product,
                    "description": description,
                }
            )
            price = client.v1.prices.create(
                {
                    "currency": "rub",
                    "unit_amount": int(amount * 100),
                    "product": product["id"],
                }
            )
            session = client.v1.checkout.sessions.create(
                {
                    "success_url": "http://localhost:8000/",
                    "line_items": [{"price": price["id"], "quantity": 1}],
                    "mode": "payment",
                }
            )
            session_data = {"id": session["id"], "payment_status": session["payment_status"], "url": session["url"]}
            return session_data
        except error.CardError as e:
            return Response({"error": e.error.message}, status=status.HTTP_400_BAD_REQUEST)
        except error.RateLimitError as e:
            return Response({"error": e.error.message}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except error.InvalidRequestError as e:
            return Response({"error": e.error.message}, status=status.HTTP_400_BAD_REQUEST)
        except error.AuthenticationError as e:
            return Response({"error": e.error.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except error.APIConnectionError as e:
            return Response({"error": e.error.message}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except error.StripeError as e:
            return Response({"error": e.error.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except exceptions.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except exceptions.MethodNotAllowed as e:
            return Response({"error": str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def checkout_payment_status(id_session):
        """Проверка статуса платежа"""

        try:
            session = client.v1.checkout.sessions.retrieve(
                id_session,
            )
            return session["payment_status"]
        except error.CardError as e:
            return Response({"error": e.error.message}, status=status.HTTP_400_BAD_REQUEST)
        except error.RateLimitError as e:
            return Response({"error": e.error.message}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except error.InvalidRequestError as e:
            return Response({"error": e.error.message}, status=status.HTTP_400_BAD_REQUEST)
        except error.AuthenticationError as e:
            return Response({"error": e.error.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except error.APIConnectionError as e:
            return Response({"error": e.error.message}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except error.StripeError as e:
            return Response({"error": e.error.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except exceptions.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except exceptions.MethodNotAllowed as e:
            return Response({"error": str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def checking_last_login_date():
    """Выборка пользователей по дате входа более 30 дней"""
    print(User.objects.filter(is_active=True).count())
    blocking_list = []
    users = User.objects.filter(is_active=True)
    thirty_days = timedelta(days=30)
    current_datetime = timezone.localtime(timezone.now())
    for user in users:
        if user.is_superuser or user.is_staff or user.groups.filter(name="Модераторы").exists():
            continue
        else:
            if user.last_login is None:
                if (current_datetime - user.date_joined) > thirty_days:
                    blocking_list.append(user.pk)
            elif (current_datetime - user.last_login) > thirty_days:
                blocking_list.append(user.pk)
    if blocking_list:
        blocking.delay(blocking_list)


def blocking_user(users):
    """Блокировка пользователя с помощью флага is_active"""
    for user_pk in users:
        user = User.objects.get(pk=user_pk)
        user.is_active = False
        user.save()
