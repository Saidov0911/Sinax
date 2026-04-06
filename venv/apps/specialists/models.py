from django.db import models
from apps.core.utils import resize_image


class Specialist(models.Model):
    image = models.ImageField(upload_to='specialists/')
    name = models.CharField(max_length=100)

    position_uz = models.CharField(max_length=200)
    position_ru = models.CharField(max_length=200, blank=True)
    position_en = models.CharField(max_length=200, blank=True)

    experience_years = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Mutaxassis'
        verbose_name_plural = 'Mutaxassislar'

    def __str__(self):
        return self.name

    def get_position(self, lang='uz'):
        return getattr(self, f'position_{lang}', '') or self.position_uz

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = Specialist.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.image.name if old.image else None

        super().save(*args, **kwargs)

        if self.image:
            if is_new or old_image != self.image.name:
                resize_image(self.image.path, max_width=400, max_height=400, quality=85)