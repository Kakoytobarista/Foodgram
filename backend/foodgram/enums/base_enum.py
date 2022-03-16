import enum


class BaseEnum(enum.Enum):
    ADD_METHODS = ('GET', 'POST',)
    DEL_METHODS = ('DELETE',)
    POST_METHOD = ('POST', )
