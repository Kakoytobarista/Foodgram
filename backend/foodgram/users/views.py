from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet
from users.paginators import PageLimitPagination
from rest_framework.decorators import action
from rest_framework import status


from users.serializers import UserSubscribeSerializer


class UserViewSet(DjoserUserViewSet):
    """Работает с пользователями.
    ViewSet для работы с пользователми - вывод таковых,
    регистрация.
    Для авторизованных пользователей —
    возможность подписаться на автора рецепта.
    """
    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer

    # @action(methods=conf.ACTION_METHODS, detail=True)
    # def subscribe(self, request, id):
    #     """Создаёт/удалет связь между пользователями.
    #     Вызов метода через url: */user/<int:id>/subscribe/.
    #     Args:
    #         request (Request): Не используется.
    #         id (int, str):
    #             id пользователя, на которого желает подписаться
    #             или отписаться запращивающий пользователь.
    #     Returns:
    #         Responce: Статус подтверждающий/отклоняющий действие.
    #     """
    #     return self.add_del_obj(id, conf.SUBSCRIBE_M2M)

    @action(methods=('get',), detail=False)
    def subscriptions(self, request):
        """Список подписок пользоваетеля.
        Вызов метода через url: */user/<int:id>/subscribtions/.
        Args:
            request (Request): Не используется.
        Returns:
            Responce:
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
