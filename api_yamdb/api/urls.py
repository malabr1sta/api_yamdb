from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CreateUserViewSet, GenreViewSet,
                    GetTokenViewSet, TitleViewSet, UsersMeViewSet,
                    UsersViewSet)

router = DefaultRouter()
router.register('auth/signup', CreateUserViewSet)
router.register('users/me', UsersMeViewSet, basename='usersme')
router.register('users', UsersViewSet, basename='users')
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenViewSet.as_view()),
]
