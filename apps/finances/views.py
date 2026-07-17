from django.shortcuts import render
from django.template.loader import render_to_string
from datetime import date
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Sum

from django.views.generic import TemplateView

from apps.cycles.models.cycle import Cycle
from apps.finances.choices import CategoryType
from apps.finances.forms.transaction_form import TransactionForm
from apps.finances.models.category import Category
from apps.finances.models.transaction import Transaction

# Create your views here.

class FinancesView(LoginRequiredMixin, TemplateView):
    template_name = "finances/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month = self.request.GET.get("month")
        category = self.request.GET.get("category")
        transaction_type = self.request.GET.get("type")

        transactions = (
            Transaction.objects.filter(
                user=self.request.user,
            )
            .select_related(
                "category",
                "cycle_phase",
                "cycle_phase__phase",
            )
        )

        if month:
            transactions = transactions.filter(
                transaction_date__month=month,
            )

        if category:
            transactions = transactions.filter(
                category_id=category,
            )

        if transaction_type:
            transactions = transactions.filter(
                category__category_type=transaction_type,
            )

        transactions = transactions.order_by(
            "-transaction_date",
        )

        budget = (
            Transaction.objects.filter(
                user=self.request.user,
                category__category_type=CategoryType.EXPENSE,
            )
            .values(
                "category__name",
            )
            .annotate(
                total=Sum("amount"),
            )
        )

        income_total = (
            Transaction.objects.filter(
                user=self.request.user,
                category__category_type=CategoryType.INCOME,
            )
            .aggregate(
                total=Sum("amount"),
            )
        )

        expense_total = (
            Transaction.objects.filter(
                user=self.request.user,
                category__category_type=CategoryType.EXPENSE,
            )
            .aggregate(
                total=Sum("amount"),
            )
        )

        context["transactions"] = transactions
        context["budget"] = budget
        context["income_total"] = income_total
        context["expense_total"] = expense_total

        context["form"] = TransactionForm(
            user=self.request.user,
            category_type=CategoryType.EXPENSE,
        )

        return context
    
    
    
class AddTransactionView(LoginRequiredMixin, View):

    def post(self, request):

        active_cycle = Cycle.objects.filter(
            user=request.user,
            end_date__isnull=True,
        ).first()

        if not active_cycle:
            return JsonResponse(
                {
                    "success": False,
                    "message": "No existe un ciclo activo.",
                },
                status=400,
            )

        transaction_type = request.POST.get("type")

        form = TransactionForm(
            request.POST,
            user=request.user,
            category_type=transaction_type,
        )

        if not form.is_valid():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Hay errores en el formulario.",
                    "errors": form.errors,
                },
                status=400,
            )

        cycle_phase = active_cycle.phases.filter(
            start_date__lte=date.today(),
            end_date__gte=date.today(),
        ).first()

        if not cycle_phase:
            return JsonResponse(
                {
                    "success": False,
                    "message": "No fue posible determinar la fase del ciclo.",
                },
                status=400,
            )

        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.cycle = active_cycle
        transaction.cycle_phase = cycle_phase
        transaction.save()

        transaction_html = render_to_string(
            "finances/partials/transaction_row.html",
            {
                "transaction": transaction,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "transaction_html": transaction_html,
            }
        )


class DeleteTransactionView(LoginRequiredMixin, View):

    def post(self, request, id):

        transaction = get_object_or_404(
            Transaction,
            id=id,
            user=request.user,
        )

        transaction.delete()

        return JsonResponse(
            {
                "success": True,
            }
        )
        
class EditTransactionView(LoginRequiredMixin, View):

    def post(self, request, id):

        transaction = get_object_or_404(
            Transaction,
            id=id,
            user=request.user,
        )

        form = TransactionForm(
            request.POST,
            instance=transaction,
            user=request.user,
            category_type=transaction.category.category_type,
        )

        if not form.is_valid():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Hay errores en el formulario.",
                    "errors": form.errors,
                },
                status=400,
            )

        transaction = form.save()

        transaction_html = render_to_string(
            "finances/partials/transaction_row.html",
            {
                "transaction": transaction,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "transaction_html": transaction_html,
            }
        )