from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User

from .serializers import CustomSignUpSerializer, ObtainTokenSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomSignUpSerializer

    def post(self, request):
        # проверяем: если юзера нет - создаём его и отправляем код
        # если юзера есть - отправляем код повторно без создания
        # проблема - повторная отправка не работает...
        # потому что проверка уникальности (.is_valid) идёт раньше и
        # запрос просто не проходит
        serializer = CustomSignUpSerializer(data=request.data)
        if serializer.is_valid():
            if not User.objects.filter(
                email=request.data['email'],
                username=request.data['username']
            ).exists():
                mail.send_mail(
                    'Yamdb confirmation code',
                    '12345',
                    'from@example.com',
                    [request.data['email']],
                )
                serializer.save()
            else:
                mail.send_mail(
                    'Yambd confirmation code reminder',
                    '12345',
                    'from@example.com',
                    [request.data['email']],
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ObtainTokenSerializer

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        if request.data['confirmation_code'] != '12345':
            error = 'Invalid verification code'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
