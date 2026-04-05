from django.db import models


class FAQ(models.Model):
    question_uz = models.CharField(max_length=500)
    question_ru = models.CharField(max_length=500)
    question_en = models.CharField(max_length=500, blank=True)
    answer_uz = models.TextField()
    answer_ru = models.TextField()
    answer_en = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQlar'

    def __str__(self):
        return self.question_uz

    def get_question(self, lang='uz'):
        return getattr(self, f'question_{lang}', self.question_uz) or self.question_uz

    def get_answer(self, lang='uz'):
        return getattr(self, f'answer_{lang}', self.answer_uz) or self.answer_uz