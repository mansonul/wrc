from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.gis import forms as geoforms

from .models import Image, RaportVoluntar, Sesizare, Status

User = get_user_model()

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image",]
        widgets = {'image': forms.FileInput(attrs={
            'class': 'sr-only',
            'accept': 'image/jpg, image/jpeg, image/png, .jpg, .jpeg, .png',
            'capture': 'environment',
            'x-on:change': "files = $event.target.files;",
            'x-on:dragover': "$el.classList.add('active')",
            'x-on:dragleave': "$el.classList.remove('active')",
            'x-on:drop': "$el.classList.remove('active')"
            })}


class SesizareForm(forms.ModelForm):
    latitudine = forms.FloatField(widget=forms.NumberInput(attrs={
            'readonly': '',
            'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',                
        }))
    longitudine = forms.FloatField(widget=forms.NumberInput(attrs={
        'readonly': '',
        'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',                
        }))
    class Meta:
        model = Sesizare
        fields = ["name", "clasa", "ordin", "status", "latitudine", "longitudine", "description",]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'rows': '8'})
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitudine'].required = False
        self.fields['longitudine'].required = False


class AdaugaVoluntar(forms.ModelForm):
    class Meta:
        model = RaportVoluntar
        fields = ["voluntar", "sesizare", "preluare_sesizare"]


class CompleteazaRaport(forms.ModelForm):
    status_din_raport = forms.ModelChoiceField(
        queryset=Status.objects.prefetch_related("sesizare_status"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    numar_indivizi = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',                
        }))
    class Meta:
        model = RaportVoluntar
        fields = ["status_din_raport", "tip_conflict", "specie_identificata", "numar_indivizi", "observatii_specialist", "sesizare"]

        widgets = {
            'observatii_specialist': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'rows': '8'})
            }


class SeteazaStatus(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all()
    )
    class Meta:
        model = Status
        fields = ["status"]


class CreazaVoluntar(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'autocomplete': 'new-password'}
    ))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        'autocomplete': 'new-password'}
    ))

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-transparent py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'autocomplete': 'off'}),
            }
