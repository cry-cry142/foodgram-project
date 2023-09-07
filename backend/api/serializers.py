from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from recipes.models import User, Tag, Ingredient


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )
        extra_kwargs = {
            'password': {'required': True, 'write_only': True}
        }


class AuthenticationUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )
        extra_kwargs = {}

    def get_is_subscribed(self, obj):
        if (
            obj in self.context['followers']
        ):
            return True
        return False


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
