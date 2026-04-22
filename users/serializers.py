from rest_framework import serializers

from .models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "city",)


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Payments
        fields = "__all__"
