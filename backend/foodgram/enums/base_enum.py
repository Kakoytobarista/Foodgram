import enum


class BaseEnum(enum.Enum):
    ADD_METHODS = ('GET', 'POST',)
    GET_METHOD = 'GET'
    POST_UPDATE_METHODS = 'POST', 'PUT', 'PATCH',
    DEL_METHODS = ('DELETE',)
    DEL_POST_METHODS = ('DELETE', 'POST')
    POST_METHOD = ('POST', )
