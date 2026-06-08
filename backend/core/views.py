"""
Porsuk: Sınav Koçu — API Görünümleri (Views)

Mobil uygulamanın veri çekeceği REST API uç noktaları.
Tüm endpoint'ler herkese açıktır (AllowAny), ancak sadece
okuma (GET) veya lead/token oluşturma (POST) izinleri vardır.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import (
    ExamDate, DailyQuestion, DiagnosticTest, LeadContact,
    Announcement, AppSettings, MotivationalQuote, FormulaCard
)
from .serializers import (
    ExamDateSerializer, DailyQuestionSerializer,
    DiagnosticTestListSerializer, DiagnosticTestDetailSerializer,
    LeadContactSerializer, DeviceTokenSerializer,
    AnnouncementSerializer, AppSettingsSerializer,
    MotivationalQuoteSerializer, FormulaCardSerializer
)


class ExamDateListView(generics.ListAPIView):
    """Gelecek ve aktif sınav tarihlerini listeler."""
    serializer_class = ExamDateSerializer
    pagination_class = None

    def get_queryset(self):
        return ExamDate.objects.filter(
            is_active=True,
            exam_date__gte=timezone.now()
        ).order_by('exam_date')


class DailyQuestionLatestView(APIView):
    """Bugünün sorusunu veya en son aktif olan soruyu getirir."""

    def get(self, request):
        today = timezone.now().date()
        
        # Önce bugünün sorusunu ara
        question = DailyQuestion.objects.filter(
            is_active=True,
            date=today
        ).first()

        # Eğer yoksa, geçmişteki en son soruyu getir
        if not question:
            question = DailyQuestion.objects.filter(
                is_active=True,
                date__lte=today
            ).order_by('-date').first()

        if question:
            serializer = DailyQuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
            
        return Response(
            {"detail": "Aktif soru bulunamadı."},
            status=status.HTTP_404_NOT_FOUND
        )


class DiagnosticTestListView(generics.ListAPIView):
    """Aktif teşhis testlerini listeler (sorular hariç)."""
    serializer_class = DiagnosticTestListSerializer
    
    def get_queryset(self):
        return DiagnosticTest.objects.filter(is_active=True)


class DiagnosticTestDetailView(generics.RetrieveAPIView):
    """Belirli bir teşhis testinin detayını (sorular dahil) getirir."""
    serializer_class = DiagnosticTestDetailSerializer
    
    def get_queryset(self):
        return DiagnosticTest.objects.filter(is_active=True)


class LeadContactCreateView(generics.CreateAPIView):
    """Uygulama içinden yeni potansiyel öğrenci (lead) kaydı oluşturur."""
    serializer_class = LeadContactSerializer
    queryset = LeadContact.objects.all()


class DeviceTokenCreateView(generics.CreateAPIView):
    """Expo push token kaydeder/günceller."""
    serializer_class = DeviceTokenSerializer


class AnnouncementListView(generics.ListAPIView):
    """Şu anda aktif olan duyuruları/banner'ları listeler."""
    serializer_class = AnnouncementSerializer
    pagination_class = None
    
    def get_queryset(self):
        now = timezone.now()
        # Aktif ve süresi geçmemiş veya süresiz olanlar
        return Announcement.objects.filter(
            is_active=True,
            start_date__lte=now
        ).exclude(
            end_date__lt=now
        ).order_by('-is_pinned', '-start_date')


class AppSettingsView(APIView):
    """Singleton uygulama ayarlarını getirir."""
    
    def get(self, request):
        settings = AppSettings.get_settings()
        serializer = AppSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data)


class MotivationalQuoteRandomView(APIView):
    """Rastgele bir aktif motivasyon sözü getirir."""
    
    def get(self, request):
        quote = MotivationalQuote.objects.filter(is_active=True).order_by('?').first()
        if quote:
            serializer = MotivationalQuoteSerializer(quote)
            return Response(serializer.data)
            
        return Response(
            {"detail": "Motivasyon sözü bulunamadı."},
            status=status.HTTP_404_NOT_FOUND
        )


class FormulaCardListView(generics.ListAPIView):
    """Formül kartlarını listeler. Opsiyonel 'topic' query parametresi ile filtrelenebilir."""
    serializer_class = FormulaCardSerializer
    pagination_class = None
    
    def get_queryset(self):
        queryset = FormulaCard.objects.filter(is_active=True)
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic=topic)
        return queryset
