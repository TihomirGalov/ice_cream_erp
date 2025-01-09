from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Report
from .publisher import publish_report_to_rabbitmq

report_created = Signal()


@receiver(report_created)
def handle_report_created(report, **kwargs):
    publish_report_to_rabbitmq(report)
