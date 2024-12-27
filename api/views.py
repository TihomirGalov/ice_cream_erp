import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from rest_framework import views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reports.models import ReportItem, Report


class IsSuperUser(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class TopSellingView(views.APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        period = request.query_params.get("period")
        start_date = datetime.date.today() - relativedelta(years=1)
        if period == "week":
            start_date = datetime.date.today() - relativedelta(weeks=1)

        if period == "month":
            start_date = datetime.date.today() - relativedelta(months=1)

        ice_creams = ReportItem.objects.filter(report__date__gte=start_date).values('ice_cream__type__name').annotate(
            total=Sum("quantity")).order_by("-total")[:10]

        names = list()
        amounts = list()
        for ice_cream in ice_creams:
            names.append(ice_cream["ice_cream__type__name"])
            amounts.append(ice_cream["total"])

        return Response({"ice_creams": names, "amounts": amounts})


class ProfitView(views.APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        period = request.query_params.get("period")
        start_date = datetime.date.today() - relativedelta(years=1)
        if period == "week":
            start_date = datetime.date.today() - relativedelta(weeks=1)

        if period == "month":
            start_date = datetime.date.today() - relativedelta(months=1)

        reports = Report.objects.filter(date__gte=start_date).values('date').annotate(total=Sum("price")).order_by(
            "date")

        dates = list()
        totals = list()

        for report in reports:
            dates.append(report["date"])
            totals.append(report["total"])

        return Response({"dates": dates, "totals": totals})


class ProfitByWorker(views.APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        start_date = datetime.date.today() - relativedelta(months=6)

        reports = Report.objects.filter(date__gte=start_date).values('store__worker__username').annotate(
            total=Sum("price")).order_by("store__worker__username")

        workers = list()
        totals = list()

        for report in reports:
            workers.append(report["store__worker__username"])
            totals.append(report["total"])

        return Response({"workers": workers, "totals": totals})


class ProfitByStore(views.APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        start_date = datetime.date.today() - relativedelta(months=6)

        reports = Report.objects.filter(date__gte=start_date).values('store__name').annotate(
            total=Sum("price")).order_by("store__name")

        stores = list()
        totals = list()

        for report in reports:
            stores.append(report["store__name"])
            totals.append(report["total"])

        return Response({"stores": stores, "totals": totals})


class DayProfits(views.APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        date = request.query_params["date"]

        reports = Report.objects.filter(date=date).values('store__name').annotate(
            total=Sum("price")).order_by("store__name")

        stores = list()
        totals = list()

        for report in reports:
            stores.append(report["store__name"])
            totals.append(report["total"])

        return Response({"stores": stores, "totals": totals})
