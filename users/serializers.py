from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "city",)
