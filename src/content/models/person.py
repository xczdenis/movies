from content.models.mixins import BaseModelWithMeta, OrjsonConfigMixin, UUIDMixin


class Person(BaseModelWithMeta, UUIDMixin, OrjsonConfigMixin):
    full_name: str

    class Meta:
        index = "persons"
