import enum


class IMAGE_TYPES(enum.Enum):
    PNG = 'png'
    JPEG = 'jpg'
    GIF = 'gif'


class FILETYPE(enum.Enum):
    TEXT = 'text'
    IMAGE = 'image'
    OTHER = 'other'


FILETYPE.IMAGES = IMAGE_TYPES
