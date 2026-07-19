from django.views.generic import TemplateView

from apps.cycles.services.cycles_service import get_dashboard_data
from apps.finances.services.transaction_service import get_transactions


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if not user.is_authenticated:
            return context

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

            # Progreso del anillo (circunferencia = 2 * pi * 54)
            circumference = 339.3
            progress = min(day / length, 1)
            context["ring_offset"] = round(
                circumference * (1 - progress), 1
            )

        return context
