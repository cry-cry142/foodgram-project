from django.contrib import admin
from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe,
    FavouriteRecipes
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'image', 'text', 'cooking_time', 'author', 'count_subscribers'
    )
    filter_vertical = ('tags',)
    inlines = [IngredientRecipeInline]
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    description = 'Рецепты'

    @admin.display(description='количество подписок')
    def count_subscribers(self, obj):
        return obj.favourite.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(FavouriteRecipes)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
