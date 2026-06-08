"""
Core app URL patterns — API endpoints.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('exam-dates/', views.ExamDateListView.as_view(), name='exam-dates-list'),
    path('daily-question/latest/', views.DailyQuestionLatestView.as_view(), name='daily-question-latest'),
    path('diagnostic-tests/', views.DiagnosticTestListView.as_view(), name='diagnostic-test-list'),
    path('diagnostic-tests/<int:pk>/', views.DiagnosticTestDetailView.as_view(), name='diagnostic-test-detail'),
    path('leads/', views.LeadContactCreateView.as_view(), name='lead-create'),
    
    # Yeni Endpoint'ler
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('settings/', views.AppSettingsView.as_view(), name='app-settings'),
    path('quotes/random/', views.MotivationalQuoteRandomView.as_view(), name='quote-random'),
    path('formulas/', views.FormulaCardListView.as_view(), name='formula-list'),
    path('device-tokens/', views.DeviceTokenCreateView.as_view(), name='device-token-create'),
]
