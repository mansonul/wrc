from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.contrib.gis.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from phonenumber_field.modelfields import PhoneNumberField

from .managers import SesizareQuerySet

import magic


ext_validator = FileExtensionValidator(['jpg', 'jpeg', 'png'])

def validate_file_mimetype(image):
    accept = ['image/png', 'image/jpg', 'image/jpeg']
    file_mimetype = magic.from_buffer(image.read(1024), mime=True)

    if file_mimetype not in accept:
        raise ValidationError('Tipul de imagine nu este suportat.')

class Image(models.Model):
    image = models.ImageField(default="vertical_bat.jpeg", validators=[ext_validator, validate_file_mimetype])


class Clasa(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    

class Ordin(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Clasa, on_delete=models.CASCADE, related_name="clasa")

    def __str__(self) -> str:
        return self.name


class CategorieTipConflict(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    

class TipConflict(models.Model):
    name = models.CharField(max_length=50)
    categorie = models.ForeignKey(CategorieTipConflict, on_delete=models.CASCADE, blank=True, null=True, related_name="categorii_conflict")

    @property
    def nume(self) -> str:
        if self.categorie:
            return self.categorie.name + ' - ' + self.name
        else:
            return self.name

    def __str__(self) -> str:
        return self.nume
    

class SpecieIdentificata(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    

class StatusCategorie(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    

class Status(models.Model):
    name = models.CharField(max_length=100)
    culoare = models.CharField(max_length=15, default="bg-red-700")
    categorie = models.ForeignKey(StatusCategorie, on_delete=models.CASCADE, blank=True, null=True, related_name="categorie_status")

    @property
    def nume(self) -> str:
        if self.categorie:
            return self.categorie.name + ' - ' + self.name
        else:
            return self.name

    def __str__(self) -> str:
        return self.nume


class Sesizare(models.Model):
    '''Raport creat de utilizatori'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="sesizare_status")
    clasa = models.ForeignKey(Clasa, on_delete=models.DO_NOTHING, blank=True, null=True)
    ordin = models.ForeignKey(Ordin, on_delete=models.DO_NOTHING, blank=True, null=True)

    name = models.CharField(max_length=30)
    location = models.PointField(null=True, blank=True)
    latitudine = models.FloatField(null=True, blank=True)
    longitudine = models.FloatField(null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    telefon = PhoneNumberField(region="RO", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # history = HistoricalRecords()

    objects = SesizareQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("reports:report_detail", kwargs={"pk": self.pk})


class Voluntar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="voluntari")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)


class RaportVoluntar(models.Model):
    '''Raport creat de voluntari pe baza sesizarilor'''
    voluntar = models.ForeignKey(Voluntar, on_delete=models.DO_NOTHING, blank=True, null=True)
    sesizare = models.ForeignKey(Sesizare, on_delete=models.SET_NULL, blank=True, null=True)
    tip_conflict = models.ForeignKey(TipConflict, on_delete=models.DO_NOTHING, null=True, blank=True)
    specie_identificata = models.ForeignKey(SpecieIdentificata, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="raport_specii")
    numar_indivizi = models.SmallIntegerField(blank=True,null=True)
    observatii_specialist = models.TextField(null=True, blank=True)
    preluare_sesizare = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    # history = HistoricalRecords()

    def __str__(self) -> str:
        return str(self.sesizare)

