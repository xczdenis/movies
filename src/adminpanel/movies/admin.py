from django.contrib import admin

from adminpanel.movies import models


class PersonFilmworkInline(admin.TabularInline):
    model = models.PersonFilmwork
    extra = 0
    autocomplete_fields = ("person",)


class GenreFilmworkInline(admin.TabularInline):
    model = models.GenreFilmwork
    extra = 0


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ("title", "type", "creation_date", "rating")
    list_filter = ("type",)
    search_fields = ("title", "description", "id")
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
    readonly_fields = ("created_at", "updated_at")
