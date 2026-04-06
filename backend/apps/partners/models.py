from django.db import models
from apps.core.utils import resize_image


class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Hamkor'
        verbose_name_plural = 'Hamkorlar'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = Partner.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.logo.name if old.logo else None

        super().save(*args, **kwargs)

        if self.logo:
            if is_new or old_image != self.logo.name:
                resize_image(self.logo.path, max_width=400, max_height=200, quality=85)