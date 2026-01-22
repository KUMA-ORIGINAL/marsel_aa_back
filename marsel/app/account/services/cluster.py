from datetime import datetime, timedelta

from django.utils import timezone

from promotions.models import Holiday

CLUSTER_GIFT_BUYERS = 'K2'
CLUSTER_FREQUENT = 'K3'
CLUSTER_DORMANT = 'K4'


def determine_cluster(user):
    now = timezone.now()
    orders = user.orders.all().order_by('created_at')

    if not orders.exists():
        return CLUSTER_DORMANT

    order_dates = [order.created_at for order in orders]
    last_order = order_dates[-1]

    # === К2: Подарочники (все покупки около праздников)
    holidays = Holiday.objects.all()
    holiday_dates = [datetime(now.year, h.month, h.day).date() for h in holidays]

    if user.birthdate:
        holiday_dates.append(user.birthdate.replace(year=now.year))

    def is_near_holiday(order_date):
        return any(abs((order_date.date() - holiday_date).days) <= 3 for holiday_date in holiday_dates)

    holiday_orders_count = sum(is_near_holiday(od) for od in order_dates)

    if holiday_orders_count == len(order_dates):
        return CLUSTER_GIFT_BUYERS

    # === К3: Частые (2+ заказа, последний ≤ 60 дней назад)
    if len(order_dates) >= 2 and (now - last_order) <= timedelta(days=60):
        return CLUSTER_FREQUENT

    # === К4: Спящие (0 или 1 заказ, или давно не покупал)
    return CLUSTER_DORMANT


def update_user_cluster(user):
    new_cluster = determine_cluster(user)

    if new_cluster and user.cluster != new_cluster:
        user.cluster = new_cluster
        user.last_cluster_update = timezone.now()

        if new_cluster == CLUSTER_DORMANT:
            user.entered_k4_at = timezone.now()
            user.welcome_discount = 5
        else:
            user.entered_k4_at = None
            user.welcome_discount = 0

        user.save(update_fields=[
            "cluster",
            "last_cluster_update",
            "entered_k4_at",
            "welcome_discount"
        ])
