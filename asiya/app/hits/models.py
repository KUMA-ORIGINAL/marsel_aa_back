from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Hit(models.Model):
    text = models.TextField(verbose_name=_("Текст"))
    photo = ProcessedImageField(
        upload_to='hits/photos/%Y/%m',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 70},
        blank=True,
        verbose_name=_("Фото")
    )
    is_hidden = models.BooleanField(default=False, verbose_name=_("Скрыт"))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Очередность"))

    class Meta:
        verbose_name = _("Хит продаж")
        verbose_name_plural = _("Хиты продаж")
        ordering = ['order']

    def __str__(self):
        return f"{self.text[:50]}"
