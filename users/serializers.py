from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2') # Добавлено first_name и last_name
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True}, # Сделали обязательными
            'last_name': {'required': True}, # Сделали обязательными
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.pop('password')) # Хешируем пароль и удаляем из validated_data
        validated_data.pop('password2') # Удаляем password2
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True) # Используем email
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password) # Аутентифицируем по email
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Пользователь неактивен.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Неверные учетные данные.")
        else:
            raise serializers.ValidationError("Необходимо указать email и пароль.")

        return data