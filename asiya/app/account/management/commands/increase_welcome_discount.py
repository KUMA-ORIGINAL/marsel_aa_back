from django.core.management.base import BaseCommand

from account.services import increase_welcome_discount


class Command(BaseCommand):
    help = "Увеличивает welcome-скидку для пользователей из кластера К4"

    def handle(self, *args, **kwargs):
        increase_welcome_discount()
        self.stdout.write(self.style.SUCCESS("Welcome-скидки успешно обновлены."))
