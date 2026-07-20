from django.urls import path

from .views import HomeView, NextDayView, PreviousDayView

app_name = "base"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("siguiente-dia/", NextDayView.as_view(), name="next-day"),
    path("dia-anterior/", PreviousDayView.as_view(), name="previous-day"),
]