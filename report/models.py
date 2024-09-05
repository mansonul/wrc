from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.gis.db import models
from django.urls import reverse

import magic


ext_validator = FileExtensionValidator(['jpg', 'jpeg', 'png'])

def validate_file_mimetype(image):
    accept = ['image/png', 'image/jpg', 'image/jpeg']
    file_mimetype = magic.from_buffer(image.read(1024), mime=True)

    if file_mimetype not in accept:
        raise ValidationError('Image type not supported.')

class Image(models.Model):
    image = models.ImageField(default="no-image.svg", validators=[ext_validator, validate_file_mimetype])


class SpeciesCategory(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    

class Specie(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(SpeciesCategory, on_delete=models.CASCADE, related_name="specii")

    def __str__(self):
        return self.name


class Report(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    # location = models.PointField(geography=True)
    location = models.PointField(null=True, blank=True)
    latitudine = models.FloatField(null=True, blank=True)
    longitudine = models.FloatField(null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    species_category = models.ForeignKey(SpeciesCategory, on_delete=models.DO_NOTHING)
    specie = models.ForeignKey(Specie, on_delete=models.DO_NOTHING)
    # status

    # @property
    # def longitude(self):
    #     return self.location.x
    
    # @property
    # def latitude(self):
    #     return self.location.y

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reports:report_detail", kwargs={"pk": self.pk})
