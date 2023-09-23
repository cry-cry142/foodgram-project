from django.contrib import admin
from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'text', 'cooking_time', 'author')
    filter_vertical = ('tags',)
    inlines = [IngredientRecipeInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
