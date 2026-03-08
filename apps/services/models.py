from django.db import models
from apps.core.utils import resize_image


class Service(models.Model):
    image = models.ImageField(upload_to='services/')

    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200, blank=True)
    name_en = models.CharField(max_length=200, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    price_label_uz = models.CharField(max_length=100, blank=True)
    price_label_ru = models.CharField(max_length=100, blank=True)
    price_label_en = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar'

    def __str__(self):
        return self.name_uz

    def get_name(self, lang='uz'):
        return getattr(self, f'name_{lang}', '') or self.name_uz

    def get_price_label(self, lang='uz'):
        return getattr(self, f'price_label_{lang}', '') or self.price_label_uz

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = Service.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.image.name if old.image else None

        super().save(*args, **kwargs)

        if self.image:
            if is_new or old_image != self.image.name:
                resize_image(self.image.path, max_width=800, max_height=600, quality=85)


