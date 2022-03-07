from django.contrib import admin

from backend.foodgram.recipes.models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('__all__',)
    list_editable = (
        'name',
        'text',
        'cooking_time',
    )
    search_fields = (
        'name',
    )
    list_filter = ('name',)
    empty_value_display = '--empty--'


class TagAdmin(admin.ModelAdmin):
    list_display = ('__all__',)
    list_editable = (
        'name',
        'color',
    )
    search_fields = (
        'name',
        'color',
    )
    list_filter = (
        'name',
        'color',
    )
    empty_value_display = '--empty--'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('__all__',)
    list_editable = (
        'name',
        'count',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    empty_value_display = '--empty--'
