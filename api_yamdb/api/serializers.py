from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

#UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=150,
        required=True,
        allow_blank=False)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, allow_blank=False,
                                      max_length=150)

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError('Username must be not "me"')

        if User.objects.filter(username=username).first():
            raise serializers.ValidationError("User already exist")

        return username

    def validate_email(self, email):
        if User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError("Email already exists!")
        return email

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        allow_blank=False)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, allow_blank=False,
                                      max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError('Username must be not "me"')

        if User.objects.filter(username=username).first():
            raise serializers.ValidationError("User already exist")

        return username

    def validate_email(self, email):
        if User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError("Email already exists!")
        return email

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')


class UserMeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        allow_blank=False)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, allow_blank=False,
                                      max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate_username(self, username):
        if username == "me":
            raise serializers.ValidationError('Username must be not "me"')
        if User.objects.filter(username=username).first():
            raise serializers.ValidationError("User already exist")
        return username

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']
