import django_filters

from django import forms
from .models import Status, Voluntar, TipConflict


class SesizareFilter(django_filters.FilterSet):
    sesizare_status = django_filters.ModelMultipleChoiceFilter(
        queryset=Status.objects.all().select_related("categorie"),
        widget=forms.CheckboxSelectMultiple(),
        field_name="status"
    )

    sesizare_voluntar = django_filters.ModelMultipleChoiceFilter(
        queryset=Voluntar.objects.all().select_related("user"),
        widget=forms.CheckboxSelectMultiple(),
        field_name="raportvoluntar__voluntar"
    )

    tip_conflict = django_filters.ModelMultipleChoiceFilter(
        queryset=TipConflict.objects.all().select_related("categorie"),
        widget=forms.CheckboxSelectMultiple(),
        field_name="raportvoluntar__tip_conflict"
    )

    start_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={
            'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
            'datepicker':'',
            'datepicker-autohide':'',
            'datepicker-buttons':'',
            'datepicker-format':"yyyy-mm-dd",
            'placeholder':"De la"
        })
    )

    end_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={
            'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
            'datepicker':'',
            'datepicker-autohide':'',
            'datepicker-buttons':'',
            'datepicker-autoselect-today':'',
            'datepicker-format':"yyyy-mm-dd",
            'placeholder':"Până la"
        })
    )

    class Meta:
        fields = ("sesizare_status", "sesizare_voluntar", "start_date", "end_date", "tip_conflict")
