from django.forms import ModelForm, PasswordInput, CharField

from .models import User


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput(), required=False)

    class Meta:
        model = User
        fields = '__all__'

    def set_password(self, obj):
        self
        return None
