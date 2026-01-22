from datetime import date

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from config import settings
from products.models import Product
from promotions.models import Holiday


def send_gift_email(user):
    now = timezone.now().date()

    holidays = Holiday.objects.all()
    selected_holidays = []
    for holiday in holidays:
        holiday_date = date(now.year, holiday.month, holiday.day)
        delta = abs((holiday_date - now).days)
        if delta <= 3:
            selected_holidays.append(holiday)

    if user.birthdate:
        birthday_this_year = user.birthdate.replace(year=now.year)
        if abs((birthday_this_year - now).days) <= 3:
            birthday_holiday = Holiday.objects.filter(name__icontains="День рождения").first()
            if birthday_holiday:
                selected_holidays.append(birthday_holiday)

    if not selected_holidays:
        return

    products = Product.objects.filter(holiday__in=selected_holidays).distinct()

    context = {
        "user": user,
        "products": products,
        "holidays": selected_holidays,
        "site_url": f"https://{settings.DOMAIN}",
    }

    # Можно выбрать шаблон универсальный, например "gift_ideas_generic.html"
    html_message = render_to_string("emails/gift_ideas_generic.html", context)
    send_mail("Идеи подарков 🎁", "", settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
