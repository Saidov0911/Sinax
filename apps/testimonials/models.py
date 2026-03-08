from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.utils import resize_image


class Testimonial(models.Model):
    avatar = models.ImageField(upload_to='testimonials/')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self):
        return f"{self.name} — {self.rating}⭐"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = Testimonial.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.avatar.name if old.avatar else None

        super().save(*args, **kwargs)

        if self.avatar:
            if is_new or old_image != self.avatar.name:
                resize_image(self.avatar.path, max_width=200, max_height=200, quality=85)