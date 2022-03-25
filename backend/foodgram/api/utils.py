from typing import Union

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import RecipeFavoriteCartSerializer, UserSubscribeSerializer
from enums.base_enum import BaseEnum
from enums.user_enum import UserEnum
from recipes.models import Recipe
from users.models import User


def get_ingredient_file(request: Request, ingredients) -> HttpResponse:
    filename: str = f'{request.user.username}_shopping_list.txt'
    shopping_list: str = f'Список покупок для: {request.user.first_name}\n\n'
    for ing in ingredients:
        shopping_list += f'{ing["ingredient__name"]}: {ing["amount"]} {ing["ingredient__measurement_unit"]}\n'

    shopping_list += '\n\nПосчитано в Foodgram'

    response = HttpResponse(shopping_list, content_type='text.txt; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def is_anonymous(user: Request) -> Response:
    if user.is_anonymous:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def is_subscribe_on_yourself(user: Request, id: str) -> Response:
    if user.id == int(id):
        return Response(
            data=UserEnum.SUBSCRIBE_ERROR_ON_YOURSELF.value,
            status=status.HTTP_400_BAD_REQUEST,
        )


def add_subscribe(user: Request, subscriber: User,
                  serializer: UserSubscribeSerializer) -> Response:
    if user.subscribe.filter(username=subscriber.username).exists():
        return Response(
            UserEnum.SUBSCRIBE_ERROR_YET_SUBSCRIBED.value,
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.subscribe.add(subscriber)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def del_subscriber(user: Request,
                   subscriber: User) -> Response:
    if not user.subscribe.filter(username=subscriber.username).exists():
        return Response(
            UserEnum.SUBSCRIBE_ERROR_DELETE_NOTHING.value,
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.subscribe.remove(subscriber)
    return Response(status=status.HTTP_204_NO_CONTENT)


def is_favorite(recipe: Recipe, user: User) -> bool:
    return recipe.favorite.filter(username=user.username)


def is_in_cart(recipe: Recipe, user: User) -> bool:
    return recipe.in_cart.filter(username=user.username)


def add_favorite(recipe: Recipe, user: User):
    recipe.favorite.add(user)


def add_in_cart(recipe: Recipe, user: User):
    recipe.in_cart.add(user)


def del_from_favorite(recipe: Recipe, user: User):
    recipe.favorite.remove(user)


def del_from_cart(recipe: Recipe, user: User):
    recipe.in_cart.remove(user)


def add_delete_favorite_in_cart(user: User,
                                method: Union[list, tuple],
                                is_favorite_or_is_in_cart: Union[is_favorite, is_in_cart],
                                add_favorite_or_cart: Union[add_favorite, add_in_cart],
                                delete_favorite_or_cart: Union[del_from_favorite, del_from_cart],
                                add_error_message: str,
                                del_error_message: str,
                                pk: int) -> Response:
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
