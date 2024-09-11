from django import forms
from django.contrib.gis import forms as geoforms
from leaflet.forms.widgets import LeafletWidget

from .models import Image, Report


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image",]
        widgets = {'image': forms.FileInput(attrs={
            'class': 'sr-only',
            'accept': 'image/jpg, image/jpeg, image/png',
            'capture': 'environment',
            'x-on:change': "files = $event.target.files;",
            'x-on:dragover': "$el.classList.add('active')",
            'x-on:dragleave': "$el.classList.remove('active')",
            'x-on:drop': "$el.classList.remove('active')"
            })}


class ReportForm(geoforms.ModelForm):
    latitudine = forms.FloatField(widget=forms.NumberInput(attrs={
            'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',                
        }))
    longitudine = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',                
        }))
    class Meta:
        model = Report
        fields = ["name", "species_category", "specie", "location", "latitudine", "longitudine", "description",]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'autocomplete': 'off'}),
            'location': LeafletWidget(),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'rows': '8'})
            }
