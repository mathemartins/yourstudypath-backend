import datetime
from abc import ABC

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils import timezone

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse

from accounts.models import Profile

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", )
        password = data.get("password", )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('User with username and password does not exists.')
        try:
            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exists')
        return {
            'username': user.username,
            'token': jwt_token
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        error_message = ''
        fields = [
            'username',
            'firstName',
            'lastName',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering"

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def get_token(self, obj):  # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def validate(self, data):
        pw = data.get('password', )
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email', ),
            username=validated_data.get('username', ),
            first_name=validated_data.get('firstName', ),
            last_name=validated_data.get('lastName', ),
            # first_name=str(validated_data.get('fullName')).split()[0],
            # last_name=str(validated_data.get('fullName')).split()[1],
        )
        user_obj.set_password(validated_data.get('password', ))
        user_obj.is_active = True
        user_obj.save()

        profile = Profile.objects.get(user=user_obj)
        profile.save()

        return user_obj