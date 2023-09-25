from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_staff:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_staff:
            return True
        return super().has_module_perms(app_label)


class Subscriptions(models.Model):
    user = models.ForeignKey(
        'User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    follower = models.ForeignKey(
        'User',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'follower'],
                name='unique_subscriptions'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('follower')),
                name='author_cannot_subscribe_to_himself'
            ),
        ]

    def __str__(self):
        return f'"{self.follower}" subscribed to "{self.user}"'
