from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from leaflet.admin import LeafletGeoAdminMixin

from .models import Image, SpeciesCategory, Specie, Report


# @gisadmin.register(Location)
# class LocationAdminClass(LeafletGeoAdmin):
#     default_zoom = 2
#     list_display = ("latitude","longitude")
# admin.site.register(Location, LocationAdminClass)

@admin.register(Image)
class ImageAdminClass(ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
    list_display = ("image_tag",)

@admin.register(SpeciesCategory)
class SpeciesCategoryAdminClass(ModelAdmin):
    pass

@admin.register(Specie)
class SpeciesAdminClass(ModelAdmin):
    pass

@admin.register(Report)
class ReportAdminClass(LeafletGeoAdminMixin, ModelAdmin):
    # def image_tag(self, obj):
    #     return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.image.url))

    list_display = ("name","species_category","specie","location","created")