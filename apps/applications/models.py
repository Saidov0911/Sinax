from django.db import models

class AllowedUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ruxsatli foydalanuvchi'
        verbose_name_plural = 'Ruxsatli foydalanuvchilar'

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"


class Application(models.Model):
    class ServiceType(models.TextChoices):
        MASKETNIY_SETKA = 'masketniy_setka', 'Masketniy setka'
        JALYUZI = 'jalyuzi', 'Jalyuzi'
        KABINKA = 'kabinka', 'Dushovoy kabinka'
        REMONT = 'remont', 'Remont'

    class Status(models.TextChoices):
        NEW = 'new', 'Gaplashilmagan'
        IN_PROGRESS = 'in_progress', 'Telefon qilinmoqda'
        CONFIRMED = 'confirmed', 'Tasdiqlandi'
        CANCELLED = 'cancelled', 'Bekor qilindi'

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=20, choices=ServiceType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    taken_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ariza'
        verbose_name_plural = 'Arizalar'

    def __str__(self):
        return f"{self.name} — {self.get_service_type_display()}"


class ApplicationMessage(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='messages'
    )
    chat_id = models.BigIntegerField()
    message_id = models.BigIntegerField()

    class Meta:
        unique_together = ['application', 'chat_id']