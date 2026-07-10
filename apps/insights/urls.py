from django.urls import path
from . import views

app_name = 'insights'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('insights/', views.InsightsView.as_view(), name='insights'),
    path('api/insights/ai/', views.AiInsightAjaxView.as_view(), name='ai-insight'),
]