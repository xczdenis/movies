from content.models.mixins import UUIDMixin


class PersonResponse(UUIDMixin):
    full_name: str
