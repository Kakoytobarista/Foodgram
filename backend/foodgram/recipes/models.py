from django.db import models

from enums.ingredient_enum import IngredientEnum
from enums.recipe_enum import RecipeEnum
from enums.tag_enum import TagEnum
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=TagEnum.NAME_MAX_LENGTH.value,
                            verbose_name=TagEnum.NAME_VERBOSE_NAME.value)
    color = models.CharField(max_length=TagEnum.COLOR_MAX_LENGTH.value,
                             verbose_name=TagEnum.COLOR_VERBOSE_NAME.value)
    slug = models.SlugField(verbose_name=TagEnum.SLUG_VERBOSE_NAME.value)

    class Meta:
        verbose_name = TagEnum.TAG_VERBOSE_NAME.value
        verbose_name_plural = TagEnum.TAG_VERBOSE_NAME_PLURAL.value


class Ingredient(models.Model):
    name = models.CharField(max_length=IngredientEnum.NAME_MAX_LENGTH.value,
                            verbose_name=IngredientEnum.NAME_VERBOSE_NAME.value)
    count = models.IntegerField(verbose_name=IngredientEnum.COUNT_VERBOSE_NAME.value)
    measurement_unit = models.CharField(max_length=IngredientEnum.MEASUREMENT_UNIT_MAX_LENGTH.value,
                                        verbose_name=IngredientEnum.MEASUREMENT_UNIT_VERBOSE_NAME.value)

    class Meta:
        verbose_name = IngredientEnum.INGREDIENT_VERBOSE_NAME.value
        verbose_name_plural = IngredientEnum.INGREDIENT_VERBOSE_NAME_PLURAL.value


class Recipe(models.Model):
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name=RecipeEnum.AUTHOR_RELATED_NAME.value,
                               verbose_name=RecipeEnum.AUTHOR_VERBOSE_NAME.value)
    name = models.CharField(max_length=RecipeEnum.NAME_MAX_LENGTH.value,
                            verbose_name=RecipeEnum.NAME_VERBOSE_NAME.value)
    image = models.ImageField(verbose_name=RecipeEnum.IMAGE_VERBOSE_NAME.value)
    text = models.TextField(verbose_name=RecipeEnum.TEXT_VERBOSE_NAME.value)
    ingredients = models.ManyToManyField(to=Ingredient,
                                         verbose_name=RecipeEnum.INGREDIENTS_VERBOSE_NAME.value,
                                         related_name=RecipeEnum.INGREDIENTS_RELATED_NAE.value)
    tags = models.ManyToManyField(to=Tag,
                                  related_name=RecipeEnum.TAGS_RELATED_NAME.value,
                                  verbose_name=RecipeEnum.TAGS_VERBOSE_NAME.value)
    cooking_time = models.IntegerField(verbose_name=RecipeEnum.COOKING_TIME.value)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name=RecipeEnum.RECIPE_PUB_DATE.value,
                                    )

    class Meta:
        verbose_name = RecipeEnum.RECIPE_VERBOSE_NAME.value
        verbose_name_plural = RecipeEnum.RECIPE_VERBOSE_NAME_PLURAL.value
        ordering = ['pub_date']
