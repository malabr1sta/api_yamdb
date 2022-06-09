from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title, User
from rest_framework import permissions

from .filter import TitleFilter
from .permissions import Admin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CreateUserSerializer,
                          GenreSerializer, TitleGetSerializer,
                          TitlePostUpdateSerializer, TokenSerializer,
                          UserMeSerializer, UserSerializer)


class GetTokenViewSet(APIView):
    serializer_class = TokenSerializer
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, username=self.request.data['username'])
        confirmation_code = request.data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def perform_create(self, serializer):
        new_user = serializer.save()
        confirmation_token = default_token_generator.make_token(new_user)
        send_mail(
            'Your verification token',
            confirmation_token,
            'from@example.com',  # Это поле "От кого"
            [new_user.email],  # Это поле "Кому" (можно указать список адресов)
            fail_silently=False,
            # Сообщать об ошибках («молчать ли об ошибках?»)
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):

    permission_classes = (Admin,)
    lookup_field = "username"
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)


class UsersMeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer()

    def list(self, request):
        queryset = User.objects.get(username=request.user)
        serializer = UserMeSerializer(queryset)
        return Response(serializer.data)

    def put(self, request):
        data = request.data
        if ('role' in request.data):
            data['role'] = request.user.role
        serializer = UserMeSerializer(
            request.user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        data1 = request.data
        if ('role' in data1):
            data1._mutable = True
            data1['role'] = request.user.role
        serializer = UserMeSerializer(request.user, data=data1, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListCreateDestroy(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):

    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(ListCreateDestroy):
    """Класс представления модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroy):
    """Класс представления модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс представления модели Title."""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ["get", "post", "delete", "patch"]
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TitleGetSerializer
        return TitlePostUpdateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        pk = serializer.data['id']
        title = Title.objects.get(id=pk)
        serializer = TitleGetSerializer(title)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        pk = serializer.data['id']
        title = Title.objects.get(id=pk)
        serializer = TitleGetSerializer(title)
        return Response(serializer.data)
