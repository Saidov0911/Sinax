from django.db import models


class GalleryItem(models.Model):
    instagram_url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return f"Gallery #{self.order}"