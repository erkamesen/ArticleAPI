from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import validators
from django.contrib.auth import password_validation

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(queryset=User.objects.all()),
    ])

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email"
        ]
