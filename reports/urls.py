from django.urls import path
from .views import create_report_view, store_form_view

app_name = "reports"

urlpatterns = [
    path("select_store/", store_form_view, name="select_store"),
    path('create_report/<int:pk>/', create_report_view, name="create_report"),
]
