from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_("Продукт")
    )
    photo = ProcessedImageField(
        upload_to='products/photos/%Y/%m',
        processors=[ResizeToFill(800, 800)],
        format='JPEG',
        options={'quality': 75},
        verbose_name=_("Фото")
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Порядок"))

    class Meta:
        verbose_name = _("Фото продукта")
        verbose_name_plural = _("Фото продуктов")
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} — {self.order}"
