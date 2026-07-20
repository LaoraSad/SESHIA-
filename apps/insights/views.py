from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.cycles.services.cycles_service import get_active_cycle
from apps.insights.services.insight_service import get_insight_history


class InsightView(LoginRequiredMixin, View):
    def get(self, request):
        active_cycle = get_active_cycle(request.user)
        insights = []

        if active_cycle:
            insights = active_cycle.insights.all()[:5]

        return render(request, "insights/detail.html", {
            "insights": insights,
        })


class InsightHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        insights = get_insight_history(request.user)
        return render(request, "insights/history.html", {
            "insights": insights,
        })