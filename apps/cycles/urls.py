from django.urls import path
from . import views

app_name = 'cycles'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('registrar/', views.RegisterPeriodView.as_view(), name='register-period'),
    path('calendario/', views.CalendarView.as_view(), name='calendar'),
    path('registro-diario/', views.DailyLogView.as_view(), name='daily-log'),
    path('historial/', views.CycleHistoryView.as_view(), name='history'),
]
