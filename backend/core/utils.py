"""
Porsuk — Admin sidebar badge callback fonksiyonları.
Unfold sidebar'da dinamik badge'ler göstermek için kullanılır.
"""

from django.utils import timezone


def exam_date_badge(request):
    """Aktif sınav sayısını badge olarak gösterir."""
    from core.models import ExamDate
    count = ExamDate.objects.filter(
        is_active=True,
        exam_date__gte=timezone.now()
    ).count()
    if count > 0:
        return count
    return None


def new_leads_badge(request):
    """İletişime geçilmemiş yeni lead sayısını badge olarak gösterir."""
    from core.models import LeadContact
    count = LeadContact.objects.filter(is_contacted=False).count()
    if count > 0:
        return count
    return None


def unsent_notifications_badge(request):
    """Gönderilmemiş bildirim sayısını badge olarak gösterir."""
    from core.models import Notification
    count = Notification.objects.filter(is_sent=False).count()
    if count > 0:
        return count
    return None


def device_count_badge(request):
    """Aktif cihaz sayısını badge olarak gösterir."""
    from core.models import DeviceToken
    count = DeviceToken.objects.filter(is_active=True).count()
    if count > 0:
        return count
    return None
