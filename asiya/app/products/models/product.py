from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название продукта"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    photo = ProcessedImageField(upload_to='products/photos/%Y/%m',
                              processors=[ResizeToFill(500, 500)],
                              format='JPEG',
                              options={'quality': 60},
                              blank=True, verbose_name=_("Фото"))
    category = models.ManyToManyField('Category', related_name='products', verbose_name=_("Категории"))
    is_hidden = models.BooleanField(default=False, verbose_name=_("Скрыт"))
    is_case = models.BooleanField(default=False, verbose_name=_("Чехол"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    def __str__(self):
        return self.name
