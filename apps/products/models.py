from django.db import models
from apps.core.utils import resize_image


class ProductCategory(models.Model):
    CATEGORY_CHOICES = [
        ('masketniy setka', 'Masketniy setka'),
        ('jalyuzi', 'Jalyuzi'),
        ('kabinka', 'Dushovoy Kabinka'),
    ]

    type = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)

    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    hero_image = models.ImageField(upload_to='categories/', blank=True, null=True)

    meta_title_uz = models.CharField(max_length=200, blank=True)
    meta_title_ru = models.CharField(max_length=200, blank=True)
    meta_title_en = models.CharField(max_length=200, blank=True)

    meta_description_uz = models.TextField(blank=True)
    meta_description_ru = models.TextField(blank=True)
    meta_description_en = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.title_uz

    def get_title(self, lang='uz'):
        return getattr(self, f'title_{lang}', '') or self.title_uz

    def get_description(self, lang='uz'):
        return getattr(self, f'description_{lang}', '') or self.description_uz

    def get_meta_title(self, lang='uz'):
        return getattr(self, f'meta_title_{lang}', '') or self.meta_title_uz

    def get_meta_description(self, lang='uz'):
        return getattr(self, f'meta_description_{lang}', '') or self.meta_description_uz

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = ProductCategory.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.hero_image.name if old.hero_image else None

        super().save(*args, **kwargs)

        if self.hero_image:
            new_image = self.hero_image.name
            if is_new or old_image != new_image:
                resize_image(self.hero_image.path, max_width=1920, max_height=1080, quality=90)


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )

    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)

    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    price_label_uz = models.CharField(max_length=100, blank=True)
    price_label_ru = models.CharField(max_length=100, blank=True)
    price_label_en = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    def __str__(self):
        return self.title_uz

    def get_title(self, lang='uz'):
        return getattr(self, f'title_{lang}', '') or self.title_uz

    def get_description(self, lang='uz'):
        return getattr(self, f'description_{lang}', '') or self.description_uz

    def get_price_label(self, lang='uz'):
        return getattr(self, f'price_label_{lang}', '') or self.price_label_uz

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None

        if not is_new:
            old = Product.objects.filter(pk=self.pk).first()
            if old:
                old_image = old.image.name if old.image else None

        super().save(*args, **kwargs)

        if self.image:
            new_image = self.image.name
            if is_new or old_image != new_image:
                resize_image(self.image.path, max_width=800, max_height=800, quality=85)