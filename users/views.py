from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)  # Разрешаем всем регистрироваться

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user_id": user.pk,
            "email": user.email
        }, status=status.HTTP_201_CREATED)  # Возвращаем 201 Created


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)  # Разрешаем всем логиниться

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Получаем пользователя из сериализатора
        return Response({
            "user_id": user.pk,
            "email": user.email
        }, status=status.HTTP_200_OK)