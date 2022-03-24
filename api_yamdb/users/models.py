from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


def max_length_role(array):
    maxi = 0
    for elem in array:
        if len(elem[0]) > maxi:
            maxi = len(elem[0])
    return maxi


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='incorrect username')])
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=max_length_role(ROLES),
                            choices=ROLES, default='user')
    confirmation_code = models.CharField(max_length=60, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["username", "email"], name="unique_user")
        ]

    def is_admin(self):
        return self.role == "admin" or self.is_staff

    def is_moderator(self):
        return self.role == "moderator"
