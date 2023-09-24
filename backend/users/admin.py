from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import User
from .forms import UserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name'
    )
    list_display_links = ('username',)
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        user = None
        if obj.id:
            user = self.model.objects.get(id=obj.id)
        if obj.password:
            obj.password = make_password(obj.password)
        obj.password = user.password
        return super().save_model(request, obj, form, change)
