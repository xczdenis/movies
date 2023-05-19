from content.models.mixins import BaseModelWithMeta, OrjsonConfigMixin, UUIDMixin


class Genre(BaseModelWithMeta, UUIDMixin, OrjsonConfigMixin):
    name: str

    class Meta:
        index = "genres"
