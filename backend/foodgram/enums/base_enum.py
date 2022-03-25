import enum


class BaseEnum(enum.Enum):
    ADD_METHODS = ('GET', 'POST',)
    GET_METHOD = 'get'
    POST_UPDATE_METHODS = 'POST', 'PUT', 'PATCH',
    DEL_METHODS = ('DELETE',)
    DEL_POST_METHODS = ('delete', 'post')
    POST_METHOD = ('POST', )
