from rest_framework import serializers

from .models import Payments, User, Subscriptions


class UserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Payments
        fields = "__all__"


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Subscriptions
        fields = "__all__"


class RetrieveUserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    payments = PaymentsSerializer(many=True)
    subscriptions = SubscriptionsSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "payments",
            "subscriptions"
        )


class GeneralInformationUserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "city",
        )
