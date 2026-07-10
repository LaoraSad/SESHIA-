from django.urls import path
from . import views

app_name = 'cycles'

urlpatterns = [
    path('cycle/', views.CycleView.as_view(), name='cycle'),
    path('api/cycles/create/', views.CycleCreateView.as_view(), name='cycle-create'),
    path('api/cycles/log-day/', views.LogDayView.as_view(), name='log-day'),
]