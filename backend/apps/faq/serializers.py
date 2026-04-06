from rest_framework import serializers
from apps.core.utils import get_lang
from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

    def get_question(self, obj):
        return obj.get_question(get_lang(self.context.get('request')))

    def get_answer(self, obj):
        return obj.get_answer(get_lang(self.context.get('request')))