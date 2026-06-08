"""
Porsuk: Sınav Koçu — Veritabanı Modelleri

Temel Modeller:
- ExamDate: Sınav tarihleri (geri sayım sayacı için)
- DailyQuestion: Günlük soru (tarih bazlı)
- DiagnosticTest: Teşhis testi (JSON tabanlı sorular)
- LeadContact: Potansiyel öğrenci bilgileri (basit CRM)

Ek Modeller:
- Notification: Push bildirim yönetimi
- DeviceToken: Cihaz token'ları (Expo Push)
- Announcement: Uygulama içi duyurular
- AppSettings: Dinamik uygulama ayarları (singleton)
- MotivationalQuote: Motivasyon sözleri
- FormulaCard: Formül Sihirbazı kartları
"""

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class ExamDate(models.Model):
    """
    YKS, LGS, MSÜ gibi sınavların tarihleri.
    Ana ekrandaki geri sayım sayacını besler.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Sınav Adı",
        help_text="Örn: YKS, LGS, MSÜ"
    )
    exam_date = models.DateTimeField(
        verbose_name="Sınav Tarihi ve Saati"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Açıklama",
        help_text="Sınav hakkında kısa bilgi (opsiyonel)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme")

    class Meta:
        verbose_name = "Sınav Tarihi"
        verbose_name_plural = "Sınav Tarihleri"
        ordering = ['exam_date']

    def __str__(self):
        return f"{self.name} — {self.exam_date.strftime('%d.%m.%Y %H:%M')}"

    @property
    def days_remaining(self):
        """Sınava kalan gün sayısı."""
        delta = self.exam_date - timezone.now()
        return max(delta.days, 0)


class DailyQuestion(models.Model):
    """
    Günün sorusu — tarih bazlı, resimli veya metin tabanlı.
    Instagram Reels çözüm linki ile birlikte.
    """

    date = models.DateField(
        unique=True,
        verbose_name="Tarih",
        help_text="Bu sorunun yayınlanacağı tarih"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Başlık",
        help_text="Örn: Zihin Açan Soru #42"
    )
    question_text = models.TextField(
        blank=True,
        verbose_name="Soru Metni",
        help_text="Metin tabanlı soru (resim yoksa)"
    )
    question_image = models.ImageField(
        upload_to='daily_questions/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Soru Görseli",
        help_text="Soru resmi (metin yoksa)"
    )
    solution_url = models.URLField(
        blank=True,
        verbose_name="Çözüm Linki",
        help_text="Instagram Reels çözüm videosu linki"
    )
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('kolay', 'Kolay'),
            ('orta', 'Orta'),
            ('zor', 'Zor'),
        ],
        default='orta',
        verbose_name="Zorluk"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme")

    class Meta:
        verbose_name = "Günün Sorusu"
        verbose_name_plural = "Günün Soruları"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} — {self.title}"


class DiagnosticTest(models.Model):
    """
    Teşhis testi — "İşlem hatası mı, bilgi eksiği mi?" analizi.
    Sorular JSON alanında tutulur, ağırlıklı cevap şıkları ile.

    questions JSON formatı:
    [
        {
            "question": "3x + 5 = 14 denkleminde x kaçtır?",
            "choices": [
                {"text": "3", "is_correct": true, "topic": "Denklemler"},
                {"text": "5", "is_correct": false, "topic": "Denklemler", "error_type": "islem_hatasi"},
                {"text": "9", "is_correct": false, "topic": "Denklemler", "error_type": "bilgi_eksigi"},
                {"text": "2", "is_correct": false, "topic": "Denklemler", "error_type": "dikkatsizlik"}
            ]
        }
    ]
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Test Başlığı",
        help_text="Örn: Temel Matematik Teşhis Testi"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Açıklama"
    )
    questions = models.JSONField(
        verbose_name="Sorular (JSON)",
        help_text="JSON formatında soru dizisi. Docstring'deki örneğe bakın.",
        default=list
    )
    target_exam = models.CharField(
        max_length=50,
        choices=[
            ('yks', 'YKS'),
            ('lgs', 'LGS'),
            ('genel', 'Genel'),
        ],
        default='genel',
        verbose_name="Hedef Sınav"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme")

    class Meta:
        verbose_name = "Teşhis Testi"
        verbose_name_plural = "Teşhis Testleri"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        """Testteki soru sayısı."""
        if isinstance(self.questions, list):
            return len(self.questions)
        return 0


class LeadContact(models.Model):
    """
    Potansiyel öğrenci — basit CRM tablosu.
    Uygulama içindeki iletişim butonlarına tıklayan veya
    test sonuçlarını gönderen öğrencilerin bilgileri.
    """

    CONTACT_SOURCE_CHOICES = [
        ('whatsapp_button', 'WhatsApp Butonu'),
        ('diagnostic_test', 'Teşhis Testi Sonucu'),
        ('free_session', 'Ücretsiz Seans Talebi'),
        ('other', 'Diğer'),
    ]

    student_name = models.CharField(
        max_length=150,
        verbose_name="Öğrenci Adı"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefon"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-posta"
    )
    contact_source = models.CharField(
        max_length=30,
        choices=CONTACT_SOURCE_CHOICES,
        default='other',
        verbose_name="İletişim Kaynağı"
    )
    weak_topics = models.JSONField(
        blank=True,
        null=True,
        default=list,
        verbose_name="Eksik Konular",
        help_text="Teşhis testinden gelen zayıf konular listesi"
    )
    diagnostic_score = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Teşhis Puanı",
        help_text="Teşhis testinden alınan puan (0-100)"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notlar",
        help_text="Öğrenci hakkında ek notlar"
    )
    is_contacted = models.BooleanField(
        default=False,
        verbose_name="İletişime geçildi mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        verbose_name = "Potansiyel Öğrenci"
        verbose_name_plural = "Potansiyel Öğrenciler"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_name} ({self.get_contact_source_display()})"


# ══════════════════════════════════════════════
# EK MODELLER
# ══════════════════════════════════════════════


class DeviceToken(models.Model):
    """
    Mobil cihaz push token'ları.
    Expo Push Notification servisi için gerekli.
    Uygulama açıldığında otomatik kaydedilir.
    """

    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Expo Push Token",
        help_text="ExponentPushToken[xxxx] formatında"
    )
    device_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cihaz Adı"
    )
    platform = models.CharField(
        max_length=20,
        choices=[
            ('android', 'Android'),
            ('ios', 'iOS'),
        ],
        default='android',
        verbose_name="Platform"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme")

    class Meta:
        verbose_name = "Cihaz Token"
        verbose_name_plural = "Cihaz Token'ları"
        ordering = ['-created_at']

    def __str__(self):
        name = self.device_name or "Bilinmeyen Cihaz"
        return f"{name} ({self.platform})"


class Notification(models.Model):
    """
    Push bildirim yönetimi.
    Admin panelinden bildirim oluştur, "Gönder" butonuna bas,
    tüm kayıtlı cihazlara Expo Push ile iletilsin.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Bildirim Başlığı",
        help_text="Örn: Yeni soru eklendi! 🎯"
    )
    body = models.TextField(
        verbose_name="Bildirim İçeriği",
        help_text="Bildirim mesajının gövdesi"
    )
    data = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name="Ek Veri (JSON)",
        help_text="Bildirime tıklanınca uygulamaya gönderilecek veri. Örn: {\"screen\": \"daily_question\"}"
    )
    send_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Gönderim Zamanı",
        help_text="Boş bırakılırsa hemen gönderilir"
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name="Gönderildi mi?"
    )
    sent_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Gönderilme Zamanı"
    )
    sent_count = models.IntegerField(
        default=0,
        verbose_name="Gönderilen Cihaz Sayısı"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")

    class Meta:
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"
        ordering = ['-created_at']

    def __str__(self):
        status = "✅ Gönderildi" if self.is_sent else "⏳ Bekliyor"
        return f"{self.title} ({status})"


class Announcement(models.Model):
    """
    Uygulama içi duyurular / banner'lar.
    Ana ekranda veya özel bir alanda gösterilir.
    Tarih aralığı ile otomatik aktif/pasif olur.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Duyuru Başlığı"
    )
    content = models.TextField(
        verbose_name="Duyuru İçeriği"
    )
    image = models.ImageField(
        upload_to='announcements/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Duyuru Görseli"
    )
    link_url = models.URLField(
        blank=True,
        verbose_name="Yönlendirme Linki",
        help_text="Duyuruya tıklanınca açılacak link (opsiyonel)"
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name="Sabitlenmiş mi?",
        help_text="Sabitlenmiş duyurular her zaman en üstte gösterilir"
    )
    start_date = models.DateTimeField(
        verbose_name="Başlangıç Tarihi",
        help_text="Duyurunun gösterilmeye başlayacağı tarih"
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Bitiş Tarihi",
        help_text="Boş bırakılırsa süresiz gösterilir"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")

    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"
        ordering = ['-is_pinned', '-start_date']

    def __str__(self):
        return self.title

    @property
    def is_currently_active(self):
        """Duyurunun şu an aktif olup olmadığını kontrol eder."""
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class AppSettings(models.Model):
    """
    Dinamik uygulama ayarları — Singleton model.
    Admin panelinden WhatsApp linki, Instagram, öğretmen profili vb.
    değiştirebilirsiniz. Uygulama güncellemeye gerek kalmaz.
    """

    # Öğretmen Profili
    teacher_name = models.CharField(
        max_length=100,
        verbose_name="Öğretmen Adı",
        default="Matematik Öğretmeni"
    )
    teacher_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Unvan / Başlık",
        help_text="Örn: Matematik Öğretmeni & Eğitim Danışmanı"
    )
    teacher_bio = models.TextField(
        blank=True,
        verbose_name="Özgeçmiş",
        help_text="Destek sekmesinde gösterilecek öğretmen biyografisi"
    )
    teacher_photo = models.ImageField(
        upload_to='teacher/',
        blank=True,
        null=True,
        verbose_name="Profil Fotoğrafı"
    )

    # İletişim Linkleri
    whatsapp_url = models.URLField(
        blank=True,
        verbose_name="WhatsApp Linki",
        help_text="Örn: https://wa.me/905XXXXXXXXX"
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Instagram Linki",
        help_text="Örn: https://instagram.com/kullaniciadi"
    )
    calendly_url = models.URLField(
        blank=True,
        verbose_name="Calendly Linki",
        help_text="Ücretsiz tanışma seansı için randevu linki"
    )
    youtube_url = models.URLField(
        blank=True,
        verbose_name="YouTube Linki"
    )
    website_url = models.URLField(
        blank=True,
        verbose_name="Web Sitesi"
    )

    # CTA Ayarları
    cta_text = models.CharField(
        max_length=200,
        default="Hala kafan mı karışık? Ücretsiz Tanışma Seansı Ayarla",
        verbose_name="CTA Buton Metni"
    )
    cta_subtitle = models.CharField(
        max_length=200,
        blank=True,
        default="İlk görüşme tamamen ücretsiz!",
        verbose_name="CTA Alt Metni"
    )

    # Genel Ayarlar
    app_name = models.CharField(
        max_length=100,
        default="Porsuk: Sınav Koçu",
        verbose_name="Uygulama Adı"
    )
    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name="Bakım Modu",
        help_text="Aktif edilirse uygulama bakım mesajı gösterir"
    )
    maintenance_message = models.TextField(
        blank=True,
        default="Uygulama şu anda bakımdadır. Kısa süre içinde geri döneceğiz!",
        verbose_name="Bakım Mesajı"
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Uygulama Ayarları"
        verbose_name_plural = "Uygulama Ayarları"

    def __str__(self):
        return "Uygulama Ayarları"

    def save(self, *args, **kwargs):
        """Singleton: Sadece bir kayıt olmasını sağlar."""
        if not self.pk and AppSettings.objects.exists():
            raise ValidationError("Sadece bir Uygulama Ayarları kaydı olabilir. Mevcut kaydı düzenleyin.")
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Ayarları getir, yoksa varsayılanlarla oluştur."""
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings


class MotivationalQuote(models.Model):
    """
    Motivasyon sözleri — uygulamada rastgele gösterilir.
    """

    quote = models.TextField(
        verbose_name="Söz",
        help_text="Motivasyon sözü metni"
    )
    author = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Söyleyen",
        help_text="Sözün sahibi (boş bırakılırsa 'Anonim' gösterilir)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")

    class Meta:
        verbose_name = "Motivasyon Sözü"
        verbose_name_plural = "Motivasyon Sözleri"
        ordering = ['-created_at']

    def __str__(self):
        author = self.author or "Anonim"
        short_quote = self.quote[:50] + "..." if len(self.quote) > 50 else self.quote
        return f'"{short_quote}" — {author}'


class FormulaCard(models.Model):
    """
    Formül Sihirbazı kartları.
    Konuya göre kategorize edilmiş formül flashcard'ları.
    """

    TOPIC_CHOICES = [
        ('temel', 'Temel Matematik'),
        ('cebir', 'Cebir'),
        ('geometri', 'Geometri'),
        ('analiz', 'Analiz'),
        ('sayilar', 'Sayılar Teorisi'),
        ('olasilik', 'Olasılık & İstatistik'),
        ('trigonometri', 'Trigonometri'),
        ('diger', 'Diğer'),
    ]

    topic = models.CharField(
        max_length=30,
        choices=TOPIC_CHOICES,
        verbose_name="Konu"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Formül Başlığı",
        help_text="Örn: Pisagor Teoremi, İkinci Dereceden Denklem Çözüm Formülü"
    )
    formula_text = models.TextField(
        verbose_name="Formül Metni",
        help_text="LaTeX veya düz metin formatında formül. Örn: a² + b² = c²"
    )
    explanation = models.TextField(
        blank=True,
        verbose_name="Açıklama",
        help_text="Formülün ne zaman ve nasıl kullanıldığına dair kısa açıklama"
    )
    formula_image = models.ImageField(
        upload_to='formulas/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Formül Görseli",
        help_text="Formülün görsel hali (opsiyonel)"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Sıralama",
        help_text="Küçük sayılar önce gösterilir"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")

    class Meta:
        verbose_name = "Formül Kartı"
        verbose_name_plural = "Formül Kartları"
        ordering = ['topic', 'order', 'title']

    def __str__(self):
        return f"[{self.get_topic_display()}] {self.title}"

