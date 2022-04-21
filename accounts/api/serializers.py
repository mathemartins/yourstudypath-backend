from django.contrib.auth import get_user_model, authenticate
from django.utils.datetime_safe import date

from rest_framework import serializers
from accounts.models import Profile

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
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
            'message',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering, Please verify your email and login"

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate(self, data):
        pw = data.get('password', )
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        print(validated_data)
        user_obj = User(
            email=validated_data.get('email', ),
            username=validated_data.get('username', ),
            first_name=validated_data.get('firstName', ),
            last_name=validated_data.get('lastName', ),
        )
        user_obj.set_password(validated_data.get('password', ))
        user_obj.is_active = True
        user_obj.save()

        profile = Profile.objects.get(user=user_obj)
        profile.save()

        return user_obj


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    image_uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'nin',
            'gender',
            'photo',
            'image_uri',
            'phone',
            'date_of_birth',
            'age',
            'slug',
            'timestamp',
            'updated',
        ]

    def get_age(self, obj: Profile):
        if obj.date_of_birth:
            today = date.today()
            return today.year - obj.date_of_birth.year - (
                    (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
        return 0

    def get_image_uri(self, obj: Profile):
        return obj.get_image

    def get_first_name(self, obj: Profile):
        return obj.user.first_name

    def get_last_name(self, obj: Profile):
        return obj.user.last_name

    def get_email(self, obj: Profile):
        return obj.user.email