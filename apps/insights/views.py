from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.cycles.services.cycles_service import get_active_cycle, get_previous_cycle
from apps.insights.services.insight_service import (
    generate_insight,
    get_latest_insight,
    get_insight_history,
)


class InsightView(LoginRequiredMixin, View):
    def get(self, request):
        active_cycle = get_active_cycle(request.user)
        insights = []

        if active_cycle:
            latest = get_latest_insight(request.user)
            if latest is None or latest.cycle != active_cycle:
                has_data = (
                    active_cycle.daily_logs.exists()
                    or active_cycle.transactions.exists()
                )
                if not has_data:
                    prev = get_previous_cycle(active_cycle)
                    has_data = prev is not None and (prev.daily_logs.exists() or prev.transactions.exists())
                if has_data:
                    generate_insight(active_cycle)
            insights = active_cycle.insights.all()

        return render(request, "insights/detail.html", {
            "insights": insights,
        })


class InsightHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        insights = get_insight_history(request.user)
        return render(request, "insights/history.html", {
            "insights": insights,
        })