from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    help = "Отправляет все активные рассылки"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status="running")

        for mailing in mailings:
            send_mailing(mailing)

        self.stdout.write(self.style.SUCCESS("Все активные рассылки отправлены"))
