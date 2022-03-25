from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import User  # isort: skip


class CustomSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(required=True,)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, value):
        username = value['username']
        if username == 'me':
            raise ValidationError("Недопустимое имя")
        return value


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
