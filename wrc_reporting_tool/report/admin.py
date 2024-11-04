from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from leaflet.admin import LeafletGeoAdminMixin

from .models import (Image, Clasa, Ordin, Sesizare, CategorieTipConflict, TipConflict, StatusCategorie, Status, Voluntar, SpecieIdentificata, RaportVoluntar)


@admin.register(RaportVoluntar)
class RaportVoluntarAdmin(ModelAdmin):
    pass


@admin.register(Image)
class ImageAdminClass(ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
    list_display = ("image_tag",)


@admin.register(SpecieIdentificata)
class SpecieIdentificataAdminClass(ModelAdmin):
    pass


@admin.register(Voluntar)
class VoluntarAdminClass(ModelAdmin):

    # list_display = ("sesizare", "sesizare__status", "user", "preluare_sesizare", "solutionare")
    # fields = ["user", "sesizare", "tip_conflict", "specie_identificata", "numar_indivizi", "observatii_specialist", ("preluare_sesizare", "solutionare")]
    pass

@admin.register(Clasa)
class ClasaAdminClass(ModelAdmin):
    pass

@admin.register(Ordin)
class OrdinAdminClass(ModelAdmin):
    pass


@admin.register(StatusCategorie)
class StatusCategorieAdminClass(ModelAdmin):
    pass

@admin.register(Status)
class StatusAdminClass(ModelAdmin):
    list_display = ["name", "culoare", "categorie"]


@admin.register(CategorieTipConflict)
class CategorieTipConflictAdminClass(ModelAdmin):
    pass

@admin.register(TipConflict)
class TipConflictAdminClass(ModelAdmin):
    pass

@admin.register(Sesizare)
class SesizareAdminClass(LeafletGeoAdminMixin, ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.image.url))

    list_display = ("name","status","clasa","ordin","location","created", "image_tag")
    exclude = ("image",)
    readonly_fields = ['image_tag']
    list_filter = ["status", "created"]
