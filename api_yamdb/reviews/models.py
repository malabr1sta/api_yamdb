from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

ROLE = (('admin', 'ADMIN'), ('moderator', 'MODERATOR'), ('user', 'USER'))


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=15, choices=ROLE, default='user')


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('id',)

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

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author} - {self.score}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author} - {self.text}'
