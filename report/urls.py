from django.urls import path

from .views import ReportList, ReportDetail, report_create, specie_partial


app_name = "reports"
urlpatterns = [
    path("add/", report_create, name="add_report"),
    path("partials/specie/", specie_partial, name="specie"),
    # path("categories/", CategoryList.as_view(), name="category_list"),
    # path("moderare/", AddsInModerationList.as_view(), name="pending"),
    # path("adauga-anunt/", AddCreate.as_view(), name="create"),
    # path("sterge/<int:pk>/", AddDelete.as_view(), name="delete"),
    # path("actualizare/<int:pk>", AddUpdate.as_view(), name="update"),
    path("<int:pk>/", ReportDetail.as_view(), name="report_detail"),
    path("", ReportList.as_view(), name="list"),
]