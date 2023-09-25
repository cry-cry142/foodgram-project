from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Subscriptions


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display_links = ('username',)
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Subscriptions)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower')
