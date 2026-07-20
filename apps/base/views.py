from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from apps.base.services.date_service import get_current_date, next_day, previous_day
from apps.cycles.services.cycles_service import get_active_cycle, get_dashboard_data
from apps.finances.services.transaction_service import get_transactions
from apps.insights.services.insight_service import generate_insight


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if not user.is_authenticated:
            return context

        context["current_date"] = get_current_date()

        transactions = get_transactions(user)

        income = sum(
            t.amount for t in transactions if t.category.is_income
        )
        spent = sum(
            t.amount for t in transactions if not t.category.is_income
        )

        context.update(get_dashboard_data(user))

        context["income"] = income
        context["spent"] = spent
        context["balance"] = income - spent
        context["recent_transactions"] = list(transactions[:4])

        cycle = context.get("active_cycle")

        if cycle:
            day = cycle.day_number
            length = cycle.expected_length

            context["cycle_day"] = day
            context["cycle_length"] = length
            context["days_to_next"] = max(length - day, 0)

            circumference = 339.3
            progress = min(day / length, 1)
            context["ring_offset"] = round(
                circumference * (1 - progress), 1
            )

        active_cycle = get_active_cycle(user)
        if active_cycle:
            context["latest_insight"] = generate_insight(active_cycle)

        return context


class NextDayView(View):
    def post(self, request):
        next_day()
        return redirect(request.POST.get("next", "base:home"))


class PreviousDayView(View):
    def post(self, request):
        previous_day()
        return redirect(request.POST.get("next", "base:home"))
