from django.db import models


class BirthdayDiscountSettings(models.Model):
    discount_percentage = models.PositiveIntegerField(verbose_name="Процент скидки")

    class Meta:
        verbose_name = "Настройка скидки на день рождение"

    def __str__(self):
        return f"{self.discount_percentage}%"
