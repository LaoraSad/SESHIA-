from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.cycles.services.cycles_service import get_active_cycle
from apps.insights.services.insight_service import (
    generate_insight,
    get_latest_insight,
    get_insight_history,
)


class InsightView(LoginRequiredMixin, View):
    def get(self, request):
        insight = get_latest_insight(request.user)

        if insight is None:
            active_cycle = get_active_cycle(request.user)
            if active_cycle:
                insight = generate_insight(active_cycle)

        return render(request, "insights/detail.html", {
            "insight": insight,
        })


class InsightHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        insights = get_insight_history(request.user)
        return render(request, "insights/history.html", {
            "insights": insights,
        })