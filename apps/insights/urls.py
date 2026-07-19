from django.urls import path
from . import views

app_name = 'insights'

urlpatterns = [
    path('', views.InsightView.as_view(), name='detail'),
    path('historial/', views.InsightHistoryView.as_view(), name='history'),
]
