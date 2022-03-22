from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    email = models.EmailField("emailaddress", unique=True)
    bio = models.TextField(max_length=500, blank=True)
    confirmation_code = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default='user')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["username", "email"],
                                    name="unique_user")
        ]

    def is_admin(self):
        return self.role == "admin" or self.is_staff

    def is_moderator(self):
        return self.role == "moderator"
