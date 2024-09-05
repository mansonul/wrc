from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.gis.geos import Point

from .forms import ImageForm, ReportForm
from .models import Report, Specie, SpeciesCategory

from wrc_reporting_tool.users.models import User


class ReportList(ListView):
    model = Report


class ReportDetail(DetailView):
    model = Report


def report_create(request):
    specii = SpeciesCategory.objects.all()
    specie = Specie.objects.all()
    if request.user.is_authenticated:
        user = request.user
    elif request.user.is_anonymous:
        user = User.objects.get(id=2)

    if request.method == "POST":
        form = ReportForm(request.POST)
        img_form = ImageForm(request.POST, request.FILES)

        if form.is_valid() and img_form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = user

            image = img_form.save()
            form_instance.image = image
            
            form_instance.location = Point(float(request.POST.get('longitudine')), float(request.POST.get('latitudine')), srid=4326)
            form_instance.save()

            return redirect("/report/")
        else:
            context = {
                'specii': specii,
                'specie': specie,
                'form': form,
                'img_form': img_form,
            }
        
    else:
        context = {
            'specii': specii,
            'specie': specie,
            'form': ReportForm(),
            'img_form': ImageForm(),
        }

    return render(request, "report/report_form.html", context=context)


def specie_partial(request):
    categorie = request.GET.get("species_category")
    specie = Specie.objects.filter(category=categorie)
    context = {"specie": specie}
    return render(request, "partials/specie.html", context)
