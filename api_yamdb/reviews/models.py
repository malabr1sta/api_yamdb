from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE = (('admin', 'ADMIN'), ('moderator', 'MODERATOR'), ('user', 'USER'))


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=15, choices=ROLE, default='user')


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='title'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='title'
    )
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    year = models.IntegerField()

    def __str__(self):
        return self.name
