from users.models import User
from auth.serializers import CustomSignUpSerializer, ObtainTokenSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomSignUpSerializer

    def post(self, request):
        serializer = CustomSignUpSerializer(data=request.data)
        if serializer.is_valid():
            if not User.objects.filter(
                email=request.data['email'],
                username=request.data['username']
            ).exists():
                mail.send_mail(
                    'Yamdb confirmation code',
                    '12346',
                    'from@example.com',
                    [request.data['email']],
                )
                serializer.save()
            else:
                mail.send_mail(
                    'Yambd confirmation code reminder',
                    '12346',
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
        if request.data['confirmation_code'] != '12346':
            error = 'Invalid verification code'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
