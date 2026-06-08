"""
Porsuk: Sınav Koçu — API Serializer'ları

Tüm modeller için DRF serializer tanımları.
"""

from rest_framework import serializers
from .models import (
    ExamDate, DailyQuestion, DiagnosticTest, LeadContact,
    DeviceToken, Notification, Announcement, AppSettings,
    MotivationalQuote, FormulaCard,
)


class ExamDateSerializer(serializers.ModelSerializer):
    days_remaining = serializers.IntegerField(read_only=True)

    class Meta:
        model = ExamDate
        fields = [
            'id', 'name', 'exam_date', 'description',
            'days_remaining',
        ]


class DailyQuestionSerializer(serializers.ModelSerializer):
    question_image_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyQuestion
        fields = [
            'id', 'date', 'title', 'question_text',
            'question_image', 'question_image_url',
            'solution_url', 'difficulty',
        ]

    def get_question_image_url(self, obj):
        """Tam URL döndür (frontend'in kolayca kullanabilmesi için)."""
        if obj.question_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.question_image.url)
            return obj.question_image.url
        return None


class DiagnosticTestListSerializer(serializers.ModelSerializer):
    """Liste görünümü — sorular dahil değil (hafif payload)."""
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DiagnosticTest
        fields = [
            'id', 'title', 'description', 'target_exam',
            'question_count',
        ]


class DiagnosticTestDetailSerializer(serializers.ModelSerializer):
    """Detay görünümü — sorular dahil."""
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DiagnosticTest
        fields = [
            'id', 'title', 'description', 'target_exam',
            'questions', 'question_count',
        ]


class LeadContactSerializer(serializers.ModelSerializer):
    """Lead oluşturma — sadece POST için."""

    class Meta:
        model = LeadContact
        fields = [
            'id', 'student_name', 'phone', 'email',
            'contact_source', 'weak_topics', 'diagnostic_score',
            'notes', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Cihaz token kayıt — POST/PUT için."""

    class Meta:
        model = DeviceToken
        fields = [
            'id', 'token', 'device_name', 'platform',
        ]

    def create(self, validated_data):
        """Token zaten varsa güncelle, yoksa oluştur."""
        token = validated_data.get('token')
        device, created = DeviceToken.objects.update_or_create(
            token=token,
            defaults={
                'device_name': validated_data.get('device_name', ''),
                'platform': validated_data.get('platform', 'android'),
                'is_active': True,
            }
        )
        return device


class AnnouncementSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    is_currently_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'image', 'image_url',
            'link_url', 'is_pinned', 'start_date', 'end_date',
            'is_currently_active',
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AppSettingsSerializer(serializers.ModelSerializer):
    teacher_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = AppSettings
        fields = [
            'teacher_name', 'teacher_title', 'teacher_bio',
            'teacher_photo', 'teacher_photo_url',
            'whatsapp_url', 'instagram_url', 'calendly_url',
            'youtube_url', 'website_url',
            'cta_text', 'cta_subtitle',
            'app_name', 'maintenance_mode', 'maintenance_message',
        ]

    def get_teacher_photo_url(self, obj):
        if obj.teacher_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.teacher_photo.url)
            return obj.teacher_photo.url
        return None


class MotivationalQuoteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = MotivationalQuote
        fields = ['id', 'quote', 'author']

    def get_author(self, obj):
        return obj.author or "Anonim"


class FormulaCardSerializer(serializers.ModelSerializer):
    topic_display = serializers.CharField(source='get_topic_display', read_only=True)
    formula_image_url = serializers.SerializerMethodField()

    class Meta:
        model = FormulaCard
        fields = [
            'id', 'topic', 'topic_display', 'title',
            'formula_text', 'explanation',
            'formula_image', 'formula_image_url', 'order',
        ]

    def get_formula_image_url(self, obj):
        if obj.formula_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.formula_image.url)
            return obj.formula_image.url
        return None
