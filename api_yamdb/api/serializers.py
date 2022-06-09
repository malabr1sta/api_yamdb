import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, User

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


class CategorySerializer(serializers.ModelSerializer):
    """Класс преобразует данные моддели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Класс преобразует данные моддели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleGetSerializer(serializers.ModelSerializer):
    """Класс преобразует данные моддели Title, при GET запросе."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostUpdateSerializer(serializers.ModelSerializer):
    """Класс преобразует данные моддели Title,
       при POST, PATCH, DELETE запросах."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError('Фильм еще не вышел.')
        return value

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
        genres = validated_data.pop('genre')
        genres = tuple(genres)
        title = Title.objects.create(**validated_data)
        title.genre.add(*genres)
        return title
