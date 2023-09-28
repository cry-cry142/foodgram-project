from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from colorfield.fields import ColorField

from .utils import upload_to

User = get_user_model()


class Tag(models.Model):
    """
    Модель "Тегов" для рецепта.
    """
    name = models.CharField('Название', max_length=200)
    color = ColorField('Цвет', max_length=7)
    slug = models.SlugField('Слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.CheckConstraint(
                check=models.Q(color__regex=r'^#[a-fA-F0-9]{6}$'),
                name='color_in_HEX'
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """
    Модель "Рецептов".
    """
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(
        'Изображение',
        upload_to=upload_to,
        null=True,
        default=None
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги'
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки',
        validators=[MinValueValidator(1)],
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        through='IngredientRecipe'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'[ {self.id} ] {self.name}'


class Ingredient(models.Model):
    """
    Модель "Ингредиентов" для рецепта.
    """
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class IngredientRecipe(models.Model):
    """
    Промежуточная модель "Ингредиенты Рецепта".
    """
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        related_name='ingred_recipes',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        verbose_name='Ингредиент',
        related_name='ingred_recipes',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиент-Рецепт'
        verbose_name_plural = 'Ингредиенты-Рецепты'
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
    """
    Промежуточная модель "Подписок на Рецепты".
    """
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='favourite_recipes',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        related_name='favourite',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка на рецепт'
        verbose_name_plural = 'Подписки на рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            ),
        ]

    def __repr__(self):
        return self.user - self.recipe


class ShoppingCart(models.Model):
    """
    Модель "Продуктовой Корзины".
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        related_name='carts',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_carts'
            ),
        ]

    def __repr__(self):
        return self.user - self.recipe
