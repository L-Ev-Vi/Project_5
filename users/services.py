from rest_framework import status
from rest_framework.response import Response
from stripe import StripeClient, error
from rest_framework import exceptions

from config import settings

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
