from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from enums.base_enum import BaseEnum
from enums.recipe_enum import RecipeEnum
from enums.user_enum import UserEnum
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from api.filters import RecipeFilterSet
from api.mixins import ListRetrieveViewSet
from api.paginators import PageLimitPagination
from api.pemissions import IsAuthorOrStaffOrReadOnly
from api.serializers import (IngredientSerializer,
                             RecipeFavoriteCartSerializer, RecipeSerializer,
                             TagSerializer, UserSubscribeSerializer)
from api.utils import get_ingredient_file


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["delete", "post"],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def favorite(self, request, pk):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=pk)
        is_favorite = recipe.favorite.filter(username=user.username)
        serializer = RecipeFavoriteCartSerializer(recipe)
        if request.method in BaseEnum.POST_METHOD.value:
            if is_favorite:
                return Response(
                    RecipeEnum.ERROR_MESSAGE_IS_FAVORITE_YET.value,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe.favorite.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method in BaseEnum.DEL_METHODS.value:
            if not is_favorite:
                return Response(
                    RecipeEnum.ERROR_MESSAGE_IS_NOT_FAVORITE.value,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe.favorite.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["delete", "post"],
        detail=True,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=pk)
        is_in_shop = recipe.in_cart.filter(username=user.username)
        serializer = RecipeFavoriteCartSerializer(recipe)
        if request.method in BaseEnum.POST_METHOD.value:
            if is_in_shop:
                return Response(
                    RecipeEnum.ERROR_MESSAGE_IS_IN_CART_YET.value,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe.in_cart.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method in BaseEnum.DEL_METHODS.value:
            if not is_in_shop:
                return Response(
                    RecipeEnum.ERROR_MESSAGE_IS_NOT_IN_CART.value,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe.in_cart.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=[
            "get",
        ],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            IngredientRecipe.objects.filter(recipe__author_id=request.user.id)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )
        return get_ingredient_file(request=request, ingredients=ingredients)


class UserViewSet(DjoserUserViewSet):
    """Работает с пользователями.
    ViewSet для работы с пользователми - вывод таковых,
    регистрация.
    Для авторизованных пользователей —
    возможность подписаться на автора рецепта.
    """

    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer
    permission_classes = (IsAuthenticated,)

    @action(
        methods=(
            "delete",
            "post",
        ),
        detail=True,
    )
    def subscribe(self, request, id):
        """Добавляет/Удаляет связь между пользователями."""
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.id == int(id):
            return Response(
                data=UserEnum.SUBSCRIBE_ERROR_ON_YOURSELF.value,
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscriber = get_object_or_404(User, id=id)
        serializer = UserSubscribeSerializer(subscriber, many=False)
        if request.method in BaseEnum.ADD_METHODS.value:
            if user.subscribe.filter(username=subscriber.username).exists():
                return Response(
                    UserEnum.SUBSCRIBE_ERROR_YET_SUBSCRIBED.value,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.subscribe.add(subscriber)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method in BaseEnum.DEL_METHODS.value:
            if not user.subscribe.filter(username=subscriber.username).exists():
                return Response(
                    UserEnum.SUBSCRIBE_ERROR_DELETE_NOTHING.value,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.subscribe.remove(subscriber)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=("get",), detail=False)
    def subscriptions(self, request):
        """Список подписок пользоваетеля.
        Вызов метода через url: */users/subscriptions/.
        Args:
            request (Request): Не используется.
        Returns:
            Response:
                401 - для неавторизованного пользователя.
                Список подписок для авторизованного пользователя.
        """
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
