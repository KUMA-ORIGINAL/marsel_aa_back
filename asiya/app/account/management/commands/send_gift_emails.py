from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from account.models import CLUSTER_K2
from account.services import send_gift_email

User = get_user_model()


class Command(BaseCommand):
    help = "Отправка подарочных email по праздникам"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(cluster=CLUSTER_K2)
        for user in users:
            send_gift_email(user)
        self.stdout.write(self.style.SUCCESS("Отправка подарочных email по праздникам завершен"))
