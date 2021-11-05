import uuid

from django.db import models


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hash = models.CharField(
        editable=False, max_length=255, verbose_name='Идентификатор')
    proportions = models.FloatField(
        editable=False, verbose_name='Пропорции')
    image = models.ImageField(
        upload_to='image', verbose_name='Изображение')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.hash
