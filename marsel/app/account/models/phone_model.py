from django.db import models


class PhoneModel(models.Model):
    brand = models.CharField(max_length=255, verbose_name="Бренд")
    model_name = models.CharField(max_length=255, verbose_name="Модель телефона")

    def __str__(self):
        return f"{self.brand} {self.model_name}"

    class Meta:
        verbose_name = "Модель телефона"
        verbose_name_plural = "Модели телефонов"
