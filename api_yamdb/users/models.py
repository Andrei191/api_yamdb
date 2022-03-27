from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOISES = [
        (ADMIN, ADMIN),
        (USER, USER),
        (MODERATOR, MODERATOR)
    ]


class User(AbstractUser):

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=max(len(role) for role, _ in UserRole.CHOISES),
        choices=UserRole.CHOISES,
        default=UserRole.USER)
    confirmation_code = models.CharField(max_length=60, blank=True)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR
