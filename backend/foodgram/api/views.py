from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.filters import RecipeFilterSet
from api.mixins import ListRetrieveViewSet
from api.paginators import PageLimitPagination
from api.permissions import IsAuthorOrStaffOrReadOnly  # Fixed typo in the import statement
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer, UserSubscribeSerializer,
                             RecipeCreateSerializer)
from api.utils import (get_ingredient_file, is_in_cart, add_in_cart,
                       add_delete_favorite_in_cart, del_from_cart,
                       is_favorite, add_favorite, del_from_favorite, is_anonymous, is_subscribe_on_yourself,
                       add_subscribe, del_subscriber)
from enums.base_enum import BaseEnum
from enums.recipe_enum import RecipeEnum
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import User


class TagViewSet(ListRetrieveViewSet):
    """
    A view set for handling tags.
    Retrieves and lists tags. Allows anonymous access.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    """
    A view set for handling ingredients.
    Retrieves and lists ingredients. Allows anonymous access.
    Supports searching by ingredient name.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    A view set for handling recipes.
    Provides CRUD operations for recipes.
    Allows filtering, searching, and pagination.
    Requires authentication for modification operations.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.
        Uses RecipeCreateSerializer for POST and PUT requests, and RecipeSerializer for others.
        """
        if self.request.method in BaseEnum.POST_UPDATE_METHODS.value:
            return RecipeCreateSerializer
        else:
            return RecipeSerializer

    def perform_create(self, serializer):
        """
        Adds the current user as the author when creating a new recipe.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Updates the recipe with the current user as the author.
        """
        serializer.save(author=self.request.user)

    @action(methods=BaseEnum.DEL_POST_METHODS.value,
            detail=True,
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk):
        """
        Adds or removes a recipe from the user's favorites.
        """
        return add_delete_favorite_in_cart(
            user=request.user, method=request.method,
            is_favorite_or_is_in_cart=is_favorite, add_favorite_or_cart=add_favorite,
            delete_favorite_or_cart=del_from_favorite, add_error_message=RecipeEnum.ERROR_MESSAGE_IS_FAVORITE_YET.value,
            del_error_message=RecipeEnum.ERROR_MESSAGE_IS_NOT_FAVORITE.value, pk=pk)

    @action(methods=BaseEnum.DEL_POST_METHODS.value,
            detail=True,
            permission_classes=[IsAuthenticated, ],)
    def shopping_cart(self, request, pk):
        """
        Adds or removes a recipe from the user's shopping cart.
        """
        return add_delete_favorite_in_cart(
            user=request.user, method=request.method,
            is_favorite_or_is_in_cart=is_in_cart, add_favorite_or_cart=add_in_cart,
            delete_favorite_or_cart=del_from_cart, add_error_message=RecipeEnum.ERROR_MESSAGE_IS_IN_CART_YET.value,
            del_error_message=RecipeEnum.ERROR_MESSAGE_IS_NOT_IN_CART.value, pk=pk)

    @action(methods=[BaseEnum.GET_METHOD.value, ],
            detail=False,
            permission_classes=[IsAuthenticated, ],)
    def download_shopping_cart(self, request, **kwargs):
        """
        Downloads the user's shopping cart as a text file.
        """
        ingredients = (
            IngredientRecipe.objects.filter(recipe__in_cart=request.user.id)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        return get_ingredient_file(request=request, ingredients=ingredients)


class UserViewSet(DjoserUserViewSet):
    """
    Handles user-related operations.
    ViewSet for listing users and user registration.
    For authenticated users, allows subscribing to recipe authors.
    """
    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=BaseEnum.DEL_POST_METHODS.value,
            detail=True, )
    def subscribe(self, request, id):
        """
        Adds or removes a subscription between users.
        """
        user = self.request.user
        if is_anonymous(user):
            return is_anonymous(user)
        if is_subscribe_on_yourself(user, id):
            return is_subscribe_on_yourself(user, id)
        subscriber = get_object_or_404(User, id=id)
        serializer = UserSubscribeSerializer(subscriber, many=False)
        if request.method in BaseEnum.ADD_METHODS.value:
            return add_subscribe(user=user, subscriber=subscriber,
                                 serializer=serializer)
        if request.method in BaseEnum.DEL_METHODS.value:
            return del_subscriber(user=user, subscriber=subscriber)

    @action(methods=(BaseEnum.GET_METHOD.value, ), detail=False)
    def subscriptions(self, request):
        """
        Lists the subscriptions of the authenticated user.
        """
        user = self.request.user
        if is_anonymous(user):
            return is_anonymous(user)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            pages,
            many=True,
            context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)
