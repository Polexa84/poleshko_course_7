from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token  # Для создания токенов

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)  # Разрешаем всем регистрироваться

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)  # Создаем или получаем токен
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "email": user.email
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)  # Разрешаем всем логиниться

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Получаем пользователя из сериализатора
        token, created = Token.objects.get_or_create(user=user)  # Создаем или получаем токен
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "email": user.email
        }, status=status.HTTP_200_OK)