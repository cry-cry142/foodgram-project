from django.contrib import admin
from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe,
    FavouriteRecipes
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'image', 'text', 'cooking_time', 'author', 'count_favourites'
    )
    filter_vertical = ('tags',)
    inlines = [IngredientRecipeInline]
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    description = 'Рецепты'

    @admin.display(description='количество в избранном')
    def count_favourites(self, obj):
        return obj.favourite.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(FavouriteRecipes)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
