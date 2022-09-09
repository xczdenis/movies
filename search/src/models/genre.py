from models.mixins import OrjsonConfigMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonConfigMixin):
    name: str

    class Meta:
        index = "genres"
