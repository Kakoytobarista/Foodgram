from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from rest_framework.response import Response

from rest_framework.decorators import action

from api.filters import RecipeFilterSet
from api.pemissions import IsAuthorOrStaffOrReadOnly
from enums.base_enum import BaseEnum
from enums.recipe_enum import RecipeEnum
from recipes.mixins import ListRetrieveViewSet
from recipes.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeFavoriteCartSerializer
from recipes.models import Tag, Ingredient, Recipe, IngredientRecipe
from recipes.utils import get_ingredient_file
from users.paginators import PageLimitPagination


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


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

    @action(methods=['delete', 'post'], detail=True,
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=pk)
        is_favorite = recipe.favorite.filter(username=user.username)
        serializer = RecipeFavoriteCartSerializer(recipe)
        if request.method in BaseEnum.POST_METHOD.value:
            if is_favorite:
                return Response(RecipeEnum.ERROR_MESSAGE_IS_FAVORITE_YET.value,
                                status=status.HTTP_400_BAD_REQUEST)
            recipe.favorite.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method in BaseEnum.DEL_METHODS.value:
            if not is_favorite:
                return Response(RecipeEnum.ERROR_MESSAGE_IS_NOT_FAVORITE.value,
                                status=status.HTTP_400_BAD_REQUEST)
            recipe.favorite.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete', 'post'], detail=True,
            permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, pk):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=pk)
        is_in_shop = recipe.in_cart.filter(username=user.username)
        serializer = RecipeFavoriteCartSerializer(recipe)
        if request.method in BaseEnum.POST_METHOD.value:
            if is_in_shop:
                return Response(RecipeEnum.ERROR_MESSAGE_IS_IN_CART_YET.value,
                                status=status.HTTP_400_BAD_REQUEST)
            recipe.in_cart.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method in BaseEnum.DEL_METHODS.value:
            if not is_in_shop:
                return Response(RecipeEnum.ERROR_MESSAGE_IS_NOT_IN_CART.value,
                                status=status.HTTP_400_BAD_REQUEST)
            recipe.in_cart.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', ],
            detail=False,
            permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request, **kwargs):
        ingredients = IngredientRecipe.objects.filter(
            recipe__author_id=request.user.id).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        return get_ingredient_file(request=request,
                                   ingredients=ingredients)
