from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .views import create_report_view, store_form_view
from django.shortcuts import render

@staff_member_required
def charts_view(request):
    return render(request, "admin/charts.html")

app_name = "reports"

urlpatterns = [
    path("select_store/", store_form_view, name="select_store"),
    path('create_report/<int:pk>/', create_report_view, name="create_report"),
    path("charts/", charts_view, name="charts"),
]
