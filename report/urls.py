from django.urls import path

from report.views import sesizare_list, report_create, specie_partial, kmz, sesizare_detail, voluntar_signup


app_name = "reports"
urlpatterns = [
    path("add/", report_create, name="add_report"),
    path("voluntar/add/", voluntar_signup, name="add_voluntar"),
    path("partials/specie/", specie_partial, name="specie"),
    path("gis/export/gigel.kml", kmz, name="export_kmz"),
    path("<int:pk>/", sesizare_detail, name="report_detail"),
    path("", sesizare_list, name="list"),
]