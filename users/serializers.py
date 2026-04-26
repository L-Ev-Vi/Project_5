from rest_framework import serializers

from .models import User, Payments


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


class RetrieveUserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    payments = PaymentsSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "city", "payments",)


class GeneralInformationUserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = ("id", "first_name", "email", "city",)
