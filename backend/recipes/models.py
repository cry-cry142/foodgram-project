from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    tags = models.ManyToManyField(
        'Tag'
    )
    text = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(
        'Ingredient'
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()
