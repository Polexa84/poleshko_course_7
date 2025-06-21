from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data.pop('password2')
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Пользователь неактивен.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Неверные учетные данные.")
        else:
            raise serializers.ValidationError("Необходимо указать имя пользователя и пароль.")

        return data