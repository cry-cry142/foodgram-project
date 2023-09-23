from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(color__regex=r'^#[a-fA-F0-9]{6}$'),
                name='color_in_HEX'
            ),
        ]

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
        'Tag',
    )
    text = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        related_name='m2m',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        related_name='m2m',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            ),
            models.CheckConstraint(
                check=models.Q(amount__gte=1),
                name='min_amount = 1'
            ),
        ]

    def __repr__(self):
        return self.recipe - self.ingredient


class FavouriteRecipes(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favourite_recipes',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='favourite',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            ),
        ]

    def __repr__(self):
        return self.user - self.recipe


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='carts',
        on_delete=models.CASCADE,
    )

    def __repr__(self):
        return self.user - self.recipe
