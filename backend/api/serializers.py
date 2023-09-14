import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotFound
from rest_framework import serializers

from recipes.models import User, Tag, Ingredient, Recipe, IngredientRecipe


class AnonimusUserSerializer(serializers.ModelSerializer):
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


class UserSerializer(AnonimusUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(AnonimusUserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )
        extra_kwargs = {}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if (
            user.is_authenticated
            and obj.subscriptions.filter(user=user).exists()
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
        extra_kwargs = {
            'name': {'read_only': True},
            'color': {'read_only': True},
            'slug': {'read_only': True},
        }


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient', required=True
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(many=True, source='m2m')
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )
        depth = 1

    def create(self, validated_data):
        validated_data.pop('tags')
        validated_data.pop('m2m')
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']
        tags = [obj['id'] for obj in tags]
        recipe = Recipe.objects.create(**validated_data)
        try:
            recipe.tags.add(*tags)
        except IntegrityError:
            raise NotFound(detail={
                'tags': 'Один из параметров не найден.'
            })
        try:
            for ingredient in ingredients:
                ingredient_obj = Ingredient.objects.get(
                    id=ingredient.get('id')
                )
                recipe.m2m.create(
                    recipe=recipe,
                    ingredient=ingredient_obj,
                    amount=ingredient.get('amount')
                )
        except ObjectDoesNotExist:
            raise NotFound(detail={
                'ingredients': 'Один из параметров не найден.'
            })
        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('tags')
        validated_data.pop('m2m')
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']
        tags = [obj['id'] for obj in tags]

        instance.tags.clear()
        try:
            instance.tags.add(*tags)
        except IntegrityError:
            raise NotFound(detail={
                'tags': 'Один из параметров не найден.'
            })

        instance.ingredients.clear()
        try:
            for ingredient in ingredients:
                ingredient_obj = Ingredient.objects.get(
                    id=ingredient.get('id')
                )
                instance.m2m.create(
                    recipe=instance,
                    ingredient=ingredient_obj,
                    amount=ingredient.get('amount')
                )
        except ObjectDoesNotExist:
            raise NotFound(detail={
                'ingredients': 'Один из параметров не найден.'
            })
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        tags_id = data.get('tags')
        tags = []
        if tags_id:
            for tag_id in tags_id:
                tags.append({'id': tag_id})
            data['tags'] = tags
        return super().to_internal_value(data)
