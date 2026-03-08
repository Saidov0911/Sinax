from django.db import models
from apps.core.utils import resize_image


class Certificate(models.Model):
    image = models.ImageField(upload_to='certificates/')

    title_uz = models.CharField(max_length=200, blank=True, null=True)
    title_ru = models.CharField(max_length=200, blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Sertifikat'
        verbose_name_plural = 'Sertifikatlar'

    def __str__(self):
        return self.title_uz or f"Sertifikat #{self.pk}"

    def get_title(self, lang='uz'):
        return getattr(self, f'title_{lang}', None) or self.title_uz

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = Certificate.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.image.name if old.image else None

        super().save(*args, **kwargs)

        if self.image:
            if is_new or old_image != self.image.name:
                resize_image(self.image.path, max_width=800, max_height=600, quality=90)