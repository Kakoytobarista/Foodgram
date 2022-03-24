from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import RecipeFavoriteCartSerializer
from enums.base_enum import BaseEnum
from enums.recipe_enum import RecipeEnum
from recipes.models import Recipe


def get_ingredient_file(request, ingredients):
    filename = f"{request.user.username}_shopping_list.txt"
    shopping_list = f"Список покупок для: {request.user.first_name}\n\n"
    for ing in ingredients:
        shopping_list += f'{ing["ingredient__name"]}: {ing["amount"]} {ing["ingredient__measurement_unit"]}\n'

    shopping_list += "\n\nПосчитано в Foodgram"

    response = HttpResponse(shopping_list, content_type="text.txt; charset=utf-8")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def is_favorite(recipe, user):
    return recipe.favorite.filter(username=user.username)


def is_in_cart(recipe, user):
    return recipe.in_cart.filter(username=user.username)


def add_favorite(recipe, user):
    recipe.favorite.add(user)


def add_in_cart(recipe, user):
    recipe.in_cart.add(user)


def del_from_favorite(recipe, user):
    recipe.is_favorited.remove(user)


def del_from_cart(recipe, user):
    recipe.in_cart.remove(user)


def add_delete_favorite_in_cart(user, method,
                                is_favorite_or_is_in_cart, add_favorite_or_cart,
                                delete_favorite_or_cart, add_error_message,
                                del_error_message, pk):
    if user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    recipe = get_object_or_404(Recipe, id=pk)
    serializer = RecipeFavoriteCartSerializer(recipe)
    if method in BaseEnum.POST_METHOD.value:
        if is_favorite_or_is_in_cart(recipe, user):
            return Response(
                add_error_message,
                status=status.HTTP_400_BAD_REQUEST,
            )
        add_favorite_or_cart(recipe, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if method in BaseEnum.DEL_METHODS.value:
        if not is_favorite_or_is_in_cart(recipe, user):
            return Response(
                del_error_message,
                status=status.HTTP_400_BAD_REQUEST,
            )
        delete_favorite_or_cart(recipe, user)
        return Response(status=status.HTTP_204_NO_CONTENT)
