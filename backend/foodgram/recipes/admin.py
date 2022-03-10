from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'text',
        'cooking_time',
    )
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
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_display_links = (
        'name',
    )
    list_editable = (
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
    list_display = (
        'name',
        'count',
        'measurement_unit',
    )
    list_display_links = ('name',)
    list_editable = (
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    empty_value_display = '--empty--'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
