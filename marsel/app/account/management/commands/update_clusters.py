from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.services import update_user_cluster

User = get_user_model()


class Command(BaseCommand):
    help = "Обновляет кластеризацию пользователей"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            update_user_cluster(user)
        self.stdout.write(self.style.SUCCESS("Кластеры пользователей обновлены"))
