from django.db import models


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    is_free = models.BooleanField(
        default=False,
        verbose_name="Бесплатный товар"
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Товар"
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в заказе {self.order.id}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"
