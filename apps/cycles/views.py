from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.cycles.forms.cycle_form import CycleForm
from apps.cycles.forms.daily_log_form import DailyLogForm
from apps.cycles.services.cycles_service import (
    get_cycle_history,
    get_dashboard_data,
    register_period,
    create_or_update_daily_log,
)
from apps.cycles.services.daily_log_service import get_daily_logs_by_cycle


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = get_dashboard_data(request.user)

        log_form = DailyLogForm(
            instance=context["today_log"],
        )

        context["form"] = CycleForm()
        context["log_form"] = log_form
        context["symptom_categories"] = log_form.symptom_categories
        context["selected_symptoms"] = log_form.selected_symptoms

        return render(
            request,
            "cycles/dashboard.html",
            context,
        )


class RegisterPeriodView(LoginRequiredMixin, View):
    def post(self, request):
        form = CycleForm(request.POST)

        if not form.is_valid():
            context = get_dashboard_data(request.user)

            context["form"] = form
            context["log_form"] = DailyLogForm(
                instance=context["today_log"],
            )

            return render(
                request,
                "cycles/dashboard.html",
                context,
            )

        register_period(
            user=request.user,
            start_date=form.cleaned_data["start_date"],
        )

        return redirect("cycles:dashboard")


class CalendarView(LoginRequiredMixin, View):
    def get(self, request):
        cycles = get_cycle_history(request.user)

        return render(
            request,
            "cycles/calendar.html",
            {
                "cycles": cycles,
            },
        )


class DailyLogView(LoginRequiredMixin, View):
    def get(self, request):
        context = get_dashboard_data(request.user)

        form = DailyLogForm(
            instance=context["today_log"],
        )

        context["form"] = form
        context["symptom_categories"] = form.symptom_categories
        context["selected_symptoms"] = form.selected_symptoms

        return render(
            request,
            "cycles/daily_log.html",
            context,
        )

    def post(self, request):
        form = DailyLogForm(request.POST)

        if not form.is_valid():
            context = get_dashboard_data(request.user)

            context["form"] = form
            context["symptom_categories"] = form.symptom_categories
            context["selected_symptoms"] = form.selected_symptoms

            return render(
                request,
                "cycles/daily_log.html",
                context,
            )

        create_or_update_daily_log(
            user=request.user,
            energy_level=form.cleaned_data["energy_level"],
            mood=form.cleaned_data["mood"],
            notes=form.cleaned_data["notes"],
            symptoms=form.cleaned_data["symptoms"],
        )

        return redirect("base:home")


class DailyLogHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        context = get_dashboard_data(request.user)
        active_cycle = context.get("active_cycle")

        daily_logs = []
        if active_cycle:
            daily_logs = get_daily_logs_by_cycle(active_cycle)

        return render(
            request,
            "cycles/daily_log_history.html",
            {
                "daily_logs": daily_logs,
                "active_cycle": active_cycle,
            },
        )


class CycleHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        cycles = get_cycle_history(request.user)

        return render(
            request,
            "cycles/history.html",
            {
                "cycles": cycles,
            },
        )