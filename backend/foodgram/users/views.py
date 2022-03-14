from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet

from enums.base_enum import BaseEnum
from enums.user_enum import UserEnum
from users.paginators import PageLimitPagination
from rest_framework.decorators import action
from rest_framework import status


from users.serializers import UserSubscribeSerializer
from users.models import User


class UserViewSet(DjoserUserViewSet):
    """Работает с пользователями.
    ViewSet для работы с пользователми - вывод таковых,
    регистрация.
    Для авторизованных пользователей —
    возможность подписаться на автора рецепта.
    """
    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer

    @action(methods=('delete', 'post',), detail=True)  # TODO Добавить проверку на пересабскайб и на переудаление
    def subscribe(self, request, id):
        """Добавляет/Удаляет связь между пользователями."""
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.id == int(id):
            return Response(data=UserEnum.SUBSCRIBE_ERROR_ON_YOURSELF.value,
                            status=status.HTTP_400_BAD_REQUEST)
        subscriber = get_object_or_404(User, id=id)
        serializer = UserSubscribeSerializer(subscriber, many=False)
        if request.method in BaseEnum.ADD_METHODS.value:
            user.subscribe.add(subscriber)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method in BaseEnum.DEL_METHODS.value:
            user.subscribe.remove(subscriber)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('get',), detail=False)
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
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
