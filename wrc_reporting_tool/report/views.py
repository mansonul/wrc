import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.gis.db.models.functions import AsKML
from django.contrib.gis.shortcuts import render_to_kmz, render_to_kml
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from wrc_reporting_tool.users.models import User 
from wrc_reporting_tool.report.filters import SesizareFilter
from wrc_reporting_tool.report.forms import ImageForm, SesizareForm, AdaugaVoluntar, CompleteazaRaport, CreazaVoluntar
from wrc_reporting_tool.report.models import (Sesizare, Clasa, Ordin, Status, Voluntar, RaportVoluntar, TipConflict, SpecieIdentificata)

def sesizare_list(request: HttpRequest) -> HttpResponse:
    array_list = list(Sesizare.objects.values('latitudine', 'longitudine', 'status', 'status__categorie', 'status__culoare', 'name'))
    sesizari_qs = Sesizare.objects.select_related('image', 'status', 'status__categorie')
    
    paginator = Paginator(sesizari_qs, settings.SESIZARI_PAGE_SIZE)
    page = request.GET.get("page", 1)
    sesizari = paginator.get_page(page)

    context = {
        'sesizare_list': sesizari,
        'sesizari': array_list
    }

    if request.htmx:
        return render(request, 'report/partials/sesizari.html', context)

    return render(request, 'report/sesizare_list.html', context)

def sesizare_detail(request: HttpRequest, pk: int) -> HttpResponse:
    sesizare = Sesizare.objects.select_related('image', 'status', 'status__categorie', 'user').prefetch_related('raportvoluntar_set', 'raportvoluntar_set__voluntar', 'raportvoluntar_set__voluntar__user').get(pk=pk)
    raport_qs = RaportVoluntar.objects.select_related('sesizare', 'voluntar__user')

    if sesizare.raportvoluntar_set.filter(sesizare=pk).exists():
        raport = raport_qs.get(sesizare=pk)
    else:
        raport = None

    context = {
        'sesizare': sesizare,
        'raport': raport,
    }
    
    return render(request, "report/sesizare_detail.html", context)

def report_create(request: HttpRequest) -> HttpResponse:
    ordin = Ordin.objects.get(pk=1)
    user = User.objects.get(id=1)
    status = Status.objects.get(id=1)

    if request.method == "POST":
        form = SesizareForm(request.POST)
        img_form = ImageForm(request.POST, request.FILES)

        if form.is_valid() and img_form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = user

            image = img_form.save()
            form_instance.image = image
            form_instance.ordin = ordin
            form_instance.clasa = Clasa.objects.get(pk=ordin.category.pk)
            form_instance.status = status
            
            form_instance.save()

            sesizare = Sesizare.objects.first()

            email_body = {
                "nume_sesizare": sesizare.name,
                "descriere_sesizare": sesizare.description,
                "data_sesizare": sesizare.created,
                "link_sesizare": sesizare.get_absolute_url(),
                "imagine_sesizare": sesizare.image.image.url
            }

            html_message = render_to_string("emails/sesizare.html", context=email_body)
            plain_message = strip_tags(html_message)

            message1 = EmailMultiAlternatives(
                from_email="mailgun@mg.wilderness-research.org",
                subject=f"Sesizare nouă - {sesizare.name}",
                to=["volutia@gmail.com",],
                body=plain_message,
                )
            message1.attach_alternative(html_message, "text/html")
            message1.send()

            return redirect("/sesizari/")
        else:
            context = {
                'ordin': ordin,
                'form': form,
                'img_form': img_form,
            }
        
    else:
        context = {
            'ordin': ordin,
            'form': SesizareForm(),
            'img_form': ImageForm(),
        }

    return render(request, "report/report_form.html", context=context)

def specie_partial(request: HttpRequest) -> HttpResponse:
    categorie = request.GET.get("clasa_category")
    ordin = Ordin.objects.filter(category=categorie)
    context = {"ordin": ordin}
    return render(request, "partials/specie.html", context)

def index(request: HttpRequest) -> HttpResponse:
    sesizare = Sesizare.objects.filter(status__categorie=1).select_related('image')
    context = {"report_list": sesizare}

    return render(request, "base.html", context)

@login_required
def dashboard_list(request: HttpRequest) -> HttpResponse:
    sesizare_filter = SesizareFilter(
        request.GET,
        queryset=Sesizare.objects.select_related('image', 'status', 'status__categorie', 'user').prefetch_related('raportvoluntar_set', 'raportvoluntar_set__voluntar', 'raportvoluntar_set__voluntar__user', 'raportvoluntar_set__tip_conflict', 'raportvoluntar_set__tip_conflict__categorie')
    )
    paginator = Paginator(sesizare_filter.qs, settings.PAGE_SIZE)
    page = request.GET.get("page", 1)
    sesizari = paginator.page(page)

    tip_conflict = TipConflict.objects.all()
    specie_identificata = SpecieIdentificata.objects.all()
    status = sesizare_filter.qs.get_status_count()
    conflict = sesizare_filter.qs.get_conflict_count()
    context = {
        "filter": sesizare_filter,
        "conflict": conflict,
        "status": status,
        "tip_conflict": tip_conflict,
        "specie_identificata": specie_identificata,
        "sesizari": sesizari,
        "nr_sesizari": paginator,
    }

    if request.htmx:
        return render(request, "dashboard/partials/tabel_raport.html", context)

    return render(request, "dashboard/dashboard_list.html", context)

@login_required
def add_voluntar_to_sesizare(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == 'POST':
        status = Status.objects.get(id=2)
        sesizare_qs = get_object_or_404(Sesizare, pk=pk)
        voluntar_qs = Voluntar.objects.get(user=request.user)
        context = {}
        form = AdaugaVoluntar(request.POST or None)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.voluntar = voluntar_qs
            form_instance.sesizare = sesizare_qs
            form_instance.preluare_sesizare = timezone.now()
            form_instance.save()
            Sesizare.objects.filter(pk=pk).update(status=status)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        context["preia_sesizare"] = form

        return render(request, "dashboard/dashboard_list.html", context=context)
    else:
        return HttpResponseNotAllowed(["POST"])

@login_required
def completeaza_raport(request: HttpRequest, pk: int) -> HttpResponse:
    raport = get_object_or_404(RaportVoluntar, pk=pk)
    form = CompleteazaRaport(instance=raport)
    status = Status.objects.all()
    tip_conflict = TipConflict.objects.all()
    sesizare = get_object_or_404(Sesizare, pk=raport.sesizare.pk)
    specie_identificata = SpecieIdentificata.objects.all()

    if request.method == "POST":
        form = CompleteazaRaport(request.POST, instance=raport)
        
        if form.is_valid():
            instance = form.save(commit=False)
            Sesizare.objects.filter(pk=sesizare.pk).update(status=form.data['status_din_raport'])
            instance.sesizare_id = sesizare.pk
            instance.save()
            return HttpResponseRedirect("/dashboard/")

    context = {
        "completeaza_raport": form,
        "status": status,
        "tip_conflict": tip_conflict,
        "specie_identificata": specie_identificata,
        "raport": raport
    }

    if request.htmx:
        return render(request, "dashboard/partials/completeaza_raport.html", context=context)
    return HttpResponseRedirect("/")

def kmz(request):
    # getting only the Åland Islands, non-ascii character in the name
    qs = Sesizare.objects.annotate(kml=AsKML("location"))
    return render_to_kml('gis/kml/placemarks.kml', { 'places' : qs})

@login_required
def voluntar_signup(request):
    form = CreazaVoluntar()
    
    if request.method == "POST":
        form = CreazaVoluntar(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='Voluntari')

            user.groups.add(user_group)

            Voluntar.objects.create(user=user)

            return HttpResponseRedirect("/dashboard/")
        
    context = {
        "form": form
    }
        
    return render(request, "dashboard/voluntar_signup.html", context)

@login_required
def export(request):

    if request.htmx:
        return HttpResponse(headers={'HX-Redirect': request.get_full_path()})


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sesizari.csv"'

    sesizare_filter = SesizareFilter(
        request.GET,
        queryset=Sesizare.objects.select_related('image', 'status', 'status__categorie', 'user').prefetch_related('raportvoluntar_set', 'raportvoluntar_set__voluntar', 'raportvoluntar_set__voluntar__user', 'raportvoluntar_set__tip_conflict', 'raportvoluntar_set__tip_conflict__categorie')
    )
    writer = csv.writer(response)
    writer.writerow([
        'data primire sesizare',
        'sesizare',
        'latitudine',
        'longitudine',
        'descriere',
        'specie',
        'tip conflict',
        'status',
        'voluntar',
    ])

    for s in sesizare_filter.qs:
        if s._prefetched_objects_cache['raportvoluntar_set'].exists():
            voluntar = s._prefetched_objects_cache['raportvoluntar_set'][0].voluntar
            conflict = s._prefetched_objects_cache['raportvoluntar_set'][0].tip_conflict
            if conflict is None:
                conflict = 'Necompletat'
            specie = s._prefetched_objects_cache['raportvoluntar_set'][0].specie_identificata
            if specie is None:
                specie = 'Necompletat'
        else:
            voluntar = 'Nepreluat'
            conflict = 'Nepreluat'
            specie = 'Nepreluat'

        writer.writerow([s.created,s.name,s.latitudine,s.longitudine,s.description,specie,conflict,s.status,voluntar])

    return response
