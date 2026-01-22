from django.db import models


class AdSlide(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='ad_slides/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Рекламный слайд'
        verbose_name_plural = 'Рекламные слайды'

    def __str__(self):
        return self.title
