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


class Follow(models.Model):
    """
    Модель описывает подписки на авторов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'following')
        ordering = ['-id']

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.following}'
