from django.core.mail import send_mail
from rest_framework import serializers

from users.models import User

from .random_func import random_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        confirmation_code = random_code()
        user = User.objects.filter(username=username, email=email)
        sender = "Someone"
        message = f"новый код подтверждения: {confirmation_code}"
        mail_subject = "confirmation_code"
        if user:
            user.update(confirmation_code=confirmation_code)
            send_mail(mail_subject, message, sender, [email])
            raise serializers.ValidationError(
                ("Пользователь уже зарегистрирован."
                 "Новый код подтверждения Вы получите на почту"))
        return data

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Используйте другой username")
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class MeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
