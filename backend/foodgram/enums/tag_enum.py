import enum


class TagEnum(enum.Enum):
    TAG_VERBOSE_NAME = 'Tag'
    TAG_VERBOSE_NAME_PLURAL = 'Tags'
    TAGS_NAME = 'tags'

    NAME_MAX_LENGTH = 100
    NAME_VERBOSE_NAME = 'Tag name'

    COLOR_MAX_LENGTH = 50
    COLOR_VERBOSE_NAME = 'HEX-code'

    SLUG_VERBOSE_NAME = 'tag Slug'
