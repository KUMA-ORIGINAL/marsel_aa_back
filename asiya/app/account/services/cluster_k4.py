from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from account.models import User
from config import settings


def _build_site_url():
    domain = str(settings.DOMAIN).strip().rstrip("/")
    if domain.startswith("http://") or domain.startswith("https://"):
        return domain
    return f"https://{domain}"


def increase_welcome_discount():
    now = timezone.now()
    users = User.objects.filter(cluster='K4', entered_k4_at__isnull=False)

    for user in users:
        delta = now - user.entered_k4_at

        if delta.days >= 14 and user.welcome_discount < 15:
            user.welcome_discount = 15
            user.save(update_fields=["welcome_discount"])
            send_discount_notification(user, 15)

        elif delta.days >= 7 and user.welcome_discount < 10:
            user.welcome_discount = 10
            user.save(update_fields=["welcome_discount"])
            send_discount_notification(user, 10)


def send_discount_notification(user, discount):
    subject = "🎉 Ваша скидка увеличилась!"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    context = {
        "first_name": user.first_name or "друг",
        "discount": discount,
        "site_url": _build_site_url(),
    }

    # Текстовая версия (на случай, если HTML не отображается)
    text_content = f"Здравствуйте, {context['first_name']}!\n\nВаша скидка теперь {discount}%!\nПерейдите на сайт: {context['site_url']}"

    # HTML-версия письма
    html_content = render_to_string("emails/discount_notification.html", context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)