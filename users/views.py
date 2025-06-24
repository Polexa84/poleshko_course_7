from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegistrationSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)  # Разрешаем всем регистрироваться

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_serializer = TokenObtainPairSerializer(data={'email': user.email, 'password': request.data['password']})
        token_serializer.is_valid(raise_exception=True)
        return Response({
            "user_id": user.pk,
            "email": user.email,
            "tokens": token_serializer.validated_data
        }, status=status.HTTP_201_CREATED)  # Возвращаем 201 Created и токены

class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)