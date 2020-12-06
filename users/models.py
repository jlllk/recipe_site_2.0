from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField(
        'email',
        blank=False,
        unique=True,
    )
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.USER,
        max_length=50,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
