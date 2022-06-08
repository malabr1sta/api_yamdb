from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE = (('admin', 'ADMIN'), ('moderator', 'MODERATOR'), ('user', 'USER'))


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=15, choices=ROLE, default='user')
