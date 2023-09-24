from django.forms import ModelForm, PasswordInput, CharField
from django.core.exceptions import ValidationError
from .models import User


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput(), required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'is_staff', 'password'
        )

    def clean(self):
        instance = self.instance
        if not instance.id and not instance.password:
            self.add_error('password', ValidationError('Пароль обязателен.'))
        return super().clean()
