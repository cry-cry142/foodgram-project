from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    follower = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='subsriptions'
    )

    class Meta:
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
