from django.db import models


class Holiday(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название праздника")
    month = models.PositiveSmallIntegerField(verbose_name="Месяц")
    day = models.PositiveSmallIntegerField(verbose_name="День")
    products = models.ManyToManyField('products.Product', blank=True, verbose_name="Товары")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Праздник"
        verbose_name_plural = "Праздники"
