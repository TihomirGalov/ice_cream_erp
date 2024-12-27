from django.urls import path
from api.views import (
    TopSellingView,
    ProfitView,
    ProfitByWorker,
    ProfitByStore,
    DayProfits,
)


app_name = "api"

urlpatterns = [
    path("top_selling/", TopSellingView.as_view(), name="top_selling"),
    path("profit/", ProfitView.as_view(), name="profit"),
    path("worker_profits/", ProfitByWorker.as_view(), name="worker_profits"),
    path("store_profits/", ProfitByStore.as_view(), name="store_profits"),
    path("day_profits/", DayProfits.as_view(), name="day_profits"),
]
