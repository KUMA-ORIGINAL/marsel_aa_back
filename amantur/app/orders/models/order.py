from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'ожидание', 'Ожидает'
        PAID = 'оплачен', 'Оплачен'
        CANCELLED = 'отменен', 'Отменен'

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Общая стоимость"
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Скидка')
    welcome_discount = models.PositiveSmallIntegerField(default=0, verbose_name="Welcome-скидка")
    free_case_count = models.PositiveIntegerField(default=0, verbose_name='Количество бесплатных чехлов')
    status = models.CharField(
        max_length=50,
        choices=Status,
        default=Status.PENDING,
        verbose_name="Статус платежа",
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь"
    )

    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"Заказ {self.id} от {self.user.email}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_case_count(self):
        """
        Метод для подсчета количества чехлов в заказе.
        """
        case_count = self.order_items.filter(product__is_case=True).aggregate(total=models.Sum('quantity'))['total']
        return case_count if case_count else 0