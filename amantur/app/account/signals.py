from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from account.models import User
from account.services import update_user_cluster


@receiver(post_save, sender=User)
def set_initial_cluster(sender, instance, created, **kwargs):
    if created:
        instance.last_cluster_update = timezone.now()
        update_user_cluster(instance)
