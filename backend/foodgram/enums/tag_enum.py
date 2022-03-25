import enum


class TagEnum(enum.Enum):
    TAG_VERBOSE_NAME = 'Тег'
    TAG_VERBOSE_NAME_PLURAL = 'Теги'
    TAGS_NAME = 'tags'

    NAME_MAX_LENGTH = 100
    NAME_VERBOSE_NAME = 'Название тега'

    COLOR_MAX_LENGTH = 50
    COLOR_VERBOSE_NAME = 'Цветовой HEX-код'

    SLUG_VERBOSE_NAME = 'Slug тега'
