"""
Porsuk: Sınav Koçu — Admin Panel Yapılandırması

django-unfold ile modern, profesyonel bir admin paneli.
Her model için özelleştirilmiş list_display, list_filter,
search_fields, fieldsets ve tab yapıları.
"""

import json
import urllib.request

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display, action

from .models import (
    ExamDate, DailyQuestion, DiagnosticTest, LeadContact,
    DeviceToken, Notification, Announcement, AppSettings,
    MotivationalQuote, FormulaCard,
)


# ──────────────────────────────────────────────
# AUTH MODELS — Unfold ModelAdmin ile yeniden kayıt
# ──────────────────────────────────────────────
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# ══════════════════════════════════════════════
# TEMEL MODELLER
# ══════════════════════════════════════════════


# ──────────────────────────────────────────────
# SINAV TARİHLERİ
# ──────────────────────────────────────────────
@admin.register(ExamDate)
class ExamDateAdmin(ModelAdmin):
    list_display = (
        'name', 'exam_date', 'days_remaining_display',
        'show_status', 'updated_at'
    )
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('exam_date',)
    list_filter_submit = True
    ordering = ('exam_date',)

    fieldsets = (
        ('Sınav Bilgileri', {
            'fields': ('name', 'exam_date', 'description'),
            'description': 'Sınavın temel bilgilerini girin. Bu bilgiler mobil uygulamadaki geri sayım sayacını besler.',
        }),
        ('Durum', {
            'fields': ('is_active',),
        }),
    )

    @display(description="Kalan Gün", ordering="exam_date")
    def days_remaining_display(self, obj):
        days = obj.days_remaining
        if days == 0:
            return format_html(
                '<span style="color: #ef4444; font-weight: 700; '
                'background: #fef2f2; padding: 2px 10px; border-radius: 9999px; '
                'font-size: 12px;">⚡ BUGÜN!</span>'
            )
        elif days <= 7:
            return format_html(
                '<span style="color: #f97316; font-weight: 600; '
                'background: #fff7ed; padding: 2px 10px; border-radius: 9999px; '
                'font-size: 12px;">🔥 {} gün</span>', days
            )
        elif days <= 30:
            return format_html(
                '<span style="color: #eab308; font-weight: 600; '
                'background: #fefce8; padding: 2px 10px; border-radius: 9999px; '
                'font-size: 12px;">⏰ {} gün</span>', days
            )
        return format_html(
            '<span style="color: #22c55e; font-weight: 600; '
            'background: #f0fdf4; padding: 2px 10px; border-radius: 9999px; '
            'font-size: 12px;">✅ {} gün</span>', days
        )

    @display(
        description="Durum",
        label={True: "success", False: "danger"},
    )
    def show_status(self, obj):
        return obj.is_active


# ──────────────────────────────────────────────
# GÜNÜN SORUSU
# ──────────────────────────────────────────────
@admin.register(DailyQuestion)
class DailyQuestionAdmin(ModelAdmin):
    list_display = (
        'date', 'title', 'show_difficulty',
        'has_image_display', 'has_solution_display', 'show_status'
    )
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'question_text')
    list_filter_submit = True
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        ('Soru Bilgileri', {
            'fields': ('date', 'title', 'difficulty'),
            'description': 'Her tarih için yalnızca bir soru olabilir.',
        }),
        ('İçerik', {
            'fields': ('question_text', 'question_image'),
            'description': 'Metin veya görsel olarak soru ekleyin. İkisi birden de olabilir.',
        }),
        ('Çözüm', {
            'fields': ('solution_url',),
            'description': 'Instagram Reels veya YouTube çözüm videosu linki.',
        }),
        ('Durum', {
            'fields': ('is_active',),
        }),
    )

    @display(
        description="Zorluk",
        label={"kolay": "success", "orta": "warning", "zor": "danger"},
    )
    def show_difficulty(self, obj):
        return obj.difficulty

    @display(description="Durum", label={True: "success", False: "danger"})
    def show_status(self, obj):
        return obj.is_active

    @display(description="Görsel")
    def has_image_display(self, obj):
        if obj.question_image:
            return format_html(
                '<span style="color: #22c55e; font-weight: 600;">📷 Var</span>'
            )
        return format_html('<span style="color: #9ca3af;">—</span>')

    @display(description="Çözüm")
    def has_solution_display(self, obj):
        if obj.solution_url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #6366f1; '
                'font-weight: 600; text-decoration: none;">🔗 İzle</a>',
                obj.solution_url
            )
        return format_html('<span style="color: #9ca3af;">—</span>')


# ──────────────────────────────────────────────
# TEŞHİS TESTİ
# ──────────────────────────────────────────────
@admin.register(DiagnosticTest)
class DiagnosticTestAdmin(ModelAdmin):
    list_display = (
        'title', 'show_target_exam', 'question_count_display',
        'show_status', 'created_at'
    )
    list_filter = ('target_exam', 'is_active')
    search_fields = ('title', 'description')
    list_filter_submit = True
    ordering = ('-created_at',)

    fieldsets = (
        ('Test Bilgileri', {
            'fields': ('title', 'description', 'target_exam'),
        }),
        ('Sorular (JSON)', {
            'fields': ('questions',),
            'description': (
                'JSON formatında soru dizisi girin. Her soru bir obje, '
                'her obje "question" ve "choices" anahtarlarını içermelidir. '
                'Choices dizisindeki her şık: "text", "is_correct" (bool), '
                '"topic" (konu) ve "error_type" (hata türü: islem_hatasi, '
                'bilgi_eksigi, dikkatsizlik veya null) içermelidir.'
            ),
        }),
        ('Durum', {
            'fields': ('is_active',),
        }),
    )

    @display(
        description="Hedef Sınav",
        label={"yks": "info", "lgs": "warning", "genel": "success"},
    )
    def show_target_exam(self, obj):
        return obj.target_exam

    @display(description="Durum", label={True: "success", False: "danger"})
    def show_status(self, obj):
        return obj.is_active

    @display(description="Soru Sayısı")
    def question_count_display(self, obj):
        count = obj.question_count
        return format_html(
            '<span style="font-weight: 700; color: #6366f1; '
            'background: #eef2ff; padding: 2px 10px; border-radius: 9999px; '
            'font-size: 12px;">{} soru</span>', count
        )


# ──────────────────────────────────────────────
# POTANSİYEL ÖĞRENCİLER (CRM)
# ──────────────────────────────────────────────
@admin.register(LeadContact)
class LeadContactAdmin(ModelAdmin):
    list_display = (
        'student_name', 'phone', 'email',
        'show_contact_source', 'diagnostic_score_display',
        'show_contacted_status', 'created_at'
    )
    list_filter = ('contact_source', 'is_contacted', 'created_at')
    search_fields = ('student_name', 'phone', 'email')
    list_editable = ('phone',)
    list_filter_submit = True
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Öğrenci İletişim Bilgileri', {
            'fields': ('student_name', 'phone', 'email'),
        }),
        ('Kaynak & Analiz', {
            'fields': ('contact_source', 'diagnostic_score', 'weak_topics'),
        }),
        ('Takip', {
            'fields': ('is_contacted', 'notes'),
        }),
        ('Kayıt Bilgisi', {
            'fields': ('created_at',),
        }),
    )

    @display(
        description="Kaynak",
        label={
            "whatsapp_button": "success",
            "diagnostic_test": "info",
            "free_session": "warning",
            "other": "info",
        },
    )
    def show_contact_source(self, obj):
        return obj.contact_source

    @display(description="İletişim", label={True: "success", False: "danger"})
    def show_contacted_status(self, obj):
        return obj.is_contacted

    @display(description="Teşhis Puanı")
    def diagnostic_score_display(self, obj):
        if obj.diagnostic_score is None:
            return format_html('<span style="color: #9ca3af;">—</span>')
        score = obj.diagnostic_score
        if score >= 70:
            color, bg = '#22c55e', '#f0fdf4'
        elif score >= 40:
            color, bg = '#f59e0b', '#fffbeb'
        else:
            color, bg = '#ef4444', '#fef2f2'
        return format_html(
            '<span style="color: {}; font-weight: 700; '
            'background: {}; padding: 2px 10px; border-radius: 9999px; '
            'font-size: 12px;">{}/100</span>',
            color, bg, score
        )


# ══════════════════════════════════════════════
# BİLDİRİM SİSTEMİ
# ══════════════════════════════════════════════


def send_expo_push_notifications(tokens, title, body, data=None):
    """
    Expo Push Notification API'sine bildirim gönderir.
    https://docs.expo.dev/push-notifications/sending-notifications/
    """
    messages_list = []
    for token in tokens:
        message = {
            "to": token,
            "sound": "default",
            "title": title,
            "body": body,
        }
        if data:
            message["data"] = data
        messages_list.append(message)

    # Expo API'ye 100'lük gruplar halinde gönder
    sent_count = 0
    for i in range(0, len(messages_list), 100):
        chunk = messages_list[i:i + 100]
        req = urllib.request.Request(
            "https://exp.host/--/api/v2/push/send",
            data=json.dumps(chunk).encode('utf-8'),
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    sent_count += len(chunk)
        except Exception:
            pass  # Log errors in production

    return sent_count


# ──────────────────────────────────────────────
# CİHAZ TOKEN'LARI
# ──────────────────────────────────────────────
@admin.register(DeviceToken)
class DeviceTokenAdmin(ModelAdmin):
    list_display = ('device_name', 'show_platform', 'token_short', 'show_status', 'created_at')
    list_filter = ('platform', 'is_active')
    search_fields = ('token', 'device_name')
    list_filter_submit = True
    readonly_fields = ('token', 'device_name', 'platform', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Cihaz Bilgileri', {
            'fields': ('token', 'device_name', 'platform'),
        }),
        ('Durum', {
            'fields': ('is_active',),
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @display(description="Platform", label={"android": "success", "ios": "info"})
    def show_platform(self, obj):
        return obj.platform

    @display(description="Durum", label={True: "success", False: "danger"})
    def show_status(self, obj):
        return obj.is_active

    @display(description="Token")
    def token_short(self, obj):
        if len(obj.token) > 30:
            return f"{obj.token[:30]}..."
        return obj.token

    def has_add_permission(self, request):
        """Token'lar sadece API'den gelir, admin'den eklenemez."""
        return False


# ──────────────────────────────────────────────
# BİLDİRİMLER
# ──────────────────────────────────────────────
@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = (
        'title', 'body_short', 'show_sent_status',
        'sent_count', 'sent_at', 'created_at'
    )
    list_filter = ('is_sent',)
    search_fields = ('title', 'body')
    list_filter_submit = True
    readonly_fields = ('is_sent', 'sent_at', 'sent_count', 'created_at')
    ordering = ('-created_at',)
    actions_detail = ["send_notification_action"]

    fieldsets = (
        ('Bildirim İçeriği', {
            'fields': ('title', 'body'),
            'description': 'Bildirim başlığı ve içeriğini yazın. Emoji kullanabilirsiniz! 🎯',
        }),
        ('Gelişmiş Ayarlar', {
            'fields': ('data', 'send_at'),
            'classes': ('collapse',),
            'description': 'Bildirime tıklanınca uygulamada açılacak ekranı belirleyebilirsiniz.',
        }),
        ('Gönderim Durumu', {
            'fields': ('is_sent', 'sent_at', 'sent_count', 'created_at'),
        }),
    )

    @display(description="İçerik")
    def body_short(self, obj):
        if len(obj.body) > 60:
            return f"{obj.body[:60]}..."
        return obj.body

    @display(description="Durum", label={True: "success", False: "warning"})
    def show_sent_status(self, obj):
        return obj.is_sent

    @action(description="📤 Bu Bildirimi Tüm Cihazlara Gönder", url_path="send-notification")
    def send_notification_action(self, request, object_id):
        """Admin detay sayfasından tek tıkla bildirim gönder."""
        notification = Notification.objects.get(pk=object_id)

        if notification.is_sent:
            messages.warning(request, "⚠️ Bu bildirim zaten gönderilmiş!")
            return

        active_tokens = list(
            DeviceToken.objects.filter(is_active=True).values_list('token', flat=True)
        )

        if not active_tokens:
            messages.error(request, "❌ Kayıtlı aktif cihaz bulunamadı!")
            return

        sent = send_expo_push_notifications(
            tokens=active_tokens,
            title=notification.title,
            body=notification.body,
            data=notification.data,
        )

        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.sent_count = sent
        notification.save()

        messages.success(
            request,
            f"✅ Bildirim başarıyla {sent} cihaza gönderildi!"
        )


# ══════════════════════════════════════════════
# EK MODELLER
# ══════════════════════════════════════════════


# ──────────────────────────────────────────────
# DUYURULAR
# ──────────────────────────────────────────────
@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = (
        'title', 'show_pinned', 'start_date', 'end_date',
        'show_active_now', 'show_status'
    )
    list_filter = ('is_pinned', 'is_active')
    search_fields = ('title', 'content')
    list_filter_submit = True
    ordering = ('-is_pinned', '-start_date')

    fieldsets = (
        ('Duyuru İçeriği', {
            'fields': ('title', 'content', 'image', 'link_url'),
        }),
        ('Zamanlama', {
            'fields': ('start_date', 'end_date'),
            'description': 'Bitiş tarihi boş bırakılırsa duyuru süresiz gösterilir.',
        }),
        ('Ayarlar', {
            'fields': ('is_pinned', 'is_active'),
        }),
    )

    @display(description="Sabit", label={True: "warning", False: "info"})
    def show_pinned(self, obj):
        return obj.is_pinned

    @display(description="Durum", label={True: "success", False: "danger"})
    def show_status(self, obj):
        return obj.is_active

    @display(description="Şu An Aktif")
    def show_active_now(self, obj):
        if obj.is_currently_active:
            return format_html(
                '<span style="color: #22c55e; font-weight: 600;">🟢 Yayında</span>'
            )
        return format_html(
            '<span style="color: #9ca3af;">⚪ Yayında Değil</span>'
        )


# ──────────────────────────────────────────────
# UYGULAMA AYARLARI (Singleton)
# ──────────────────────────────────────────────
@admin.register(AppSettings)
class AppSettingsAdmin(ModelAdmin):
    list_display = ('__str__', 'teacher_name', 'maintenance_mode_display', 'updated_at')
    fieldsets = (
        ('👨‍🏫 Öğretmen Profili', {
            'fields': ('teacher_name', 'teacher_title', 'teacher_bio', 'teacher_photo'),
            'description': 'Destek ekranında gösterilecek öğretmen bilgileri.',
        }),
        ('🔗 İletişim Linkleri', {
            'fields': ('whatsapp_url', 'instagram_url', 'calendly_url', 'youtube_url', 'website_url'),
            'description': 'Sosyal medya ve iletişim linkleriniz.',
        }),
        ('🎯 CTA (Call To Action) Ayarları', {
            'fields': ('cta_text', 'cta_subtitle'),
            'description': 'Destek ekranındaki ana buton metinleri.',
        }),
        ('⚙️ Genel Ayarlar', {
            'fields': ('app_name', 'maintenance_mode', 'maintenance_message'),
        }),
    )

    @display(description="Bakım Modu")
    def maintenance_mode_display(self, obj):
        if obj.maintenance_mode:
            return format_html(
                '<span style="color: #ef4444; font-weight: 700; '
                'background: #fef2f2; padding: 2px 10px; border-radius: 9999px; '
                'font-size: 12px;">🔴 BAKIM MODU AKTİF</span>'
            )
        return format_html(
            '<span style="color: #22c55e; font-weight: 600; '
            'background: #f0fdf4; padding: 2px 10px; border-radius: 9999px; '
            'font-size: 12px;">🟢 Normal</span>'
        )

    def has_add_permission(self, request):
        """Singleton: Sadece bir kayıt olmasını sağla."""
        return not AppSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Ayarlar silinemez."""
        return False


# ──────────────────────────────────────────────
# MOTİVASYON SÖZLERİ
# ──────────────────────────────────────────────
@admin.register(MotivationalQuote)
class MotivationalQuoteAdmin(ModelAdmin):
    list_display = ('quote_short', 'author', 'show_status', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('quote', 'author')
    list_filter_submit = True
    ordering = ('-created_at',)

    fieldsets = (
        ('Motivasyon Sözü', {
            'fields': ('quote', 'author'),
        }),
        ('Durum', {
            'fields': ('is_active',),
        }),
    )

    @display(description="Söz")
    def quote_short(self, obj):
        if len(obj.quote) > 80:
            return f'"{obj.quote[:80]}..."'
        return f'"{obj.quote}"'

    @display(description="Durum", label={True: "success", False: "danger"})
    def show_status(self, obj):
        return obj.is_active


# ──────────────────────────────────────────────
# FORMÜL KARTLARI
# ──────────────────────────────────────────────
@admin.register(FormulaCard)
class FormulaCardAdmin(ModelAdmin):
    list_display = ('title', 'show_topic', 'formula_short', 'order', 'show_status')
    list_filter = ('topic', 'is_active')
    search_fields = ('title', 'formula_text', 'explanation')
    list_editable = ('order',)
    list_filter_submit = True
    ordering = ('topic', 'order')

    fieldsets = (
        ('Formül Bilgileri', {
            'fields': ('topic', 'title', 'order'),
        }),
        ('İçerik', {
            'fields': ('formula_text', 'explanation', 'formula_image'),
            'description': 'Formülü metin olarak girin. LaTeX formatı desteklenir. Opsiyonel olarak görsel de ekleyebilirsiniz.',
        }),
        ('Durum', {
            'fields': ('is_active',),
        }),
    )

    @display(
        description="Konu",
        label={
            "temel": "success", "cebir": "info", "geometri": "warning",
            "analiz": "danger", "sayilar": "info", "olasilik": "warning",
            "trigonometri": "success", "diger": "info",
        },
    )
    def show_topic(self, obj):
        return obj.topic

    @display(description="Formül")
    def formula_short(self, obj):
        if len(obj.formula_text) > 50:
            return f"{obj.formula_text[:50]}..."
        return obj.formula_text

    @display(description="Durum", label={True: "success", False: "danger"})
    def show_status(self, obj):
        return obj.is_active
