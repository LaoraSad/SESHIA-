
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.finances.forms.expense_form import ExpenseForm
from apps.finances.forms.category_form import CategoryForm
from apps.finances.forms.income_form import IncomeForm
from apps.finances.services.category_service import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)
from apps.finances.services.transaction_service import (
    create_transaction,
    delete_transaction,
    get_transaction,
    get_transactions,
    update_transaction,
)


# Transactions

class TransactionListView(LoginRequiredMixin, View):
    def get(self, request):
        transactions = get_transactions(request.user)
        return render(request, "finances/list.html", {
            "transactions": transactions,
        })


class CreateExpenseView(LoginRequiredMixin, View):
    def get(self, request):
        form = ExpenseForm(user=request.user)
        return render(request, "finances/form.html", {
            "form": form,
            "title": "Registrar gasto",
        })

    def post(self, request):
        form = ExpenseForm(request.POST, user=request.user)

        if not form.is_valid():
            return render(request, "finances/form.html", {
                "form": form,
                "title": "Registrar gasto",
            })

        try:
            create_transaction(
                user=request.user,
                category=form.cleaned_data["category"],
                amount=form.cleaned_data["amount"],
                transaction_date=form.cleaned_data["transaction_date"],
                description=form.cleaned_data.get("description", ""),
            )
        except ValueError as e:
            form.add_error(None, str(e))
            return render(request, "finances/form.html", {
                "form": form,
                "title": "Registrar gasto",
            })

        return redirect("finances:list")


class CreateIncomeView(LoginRequiredMixin, View):
    def get(self, request):
        form = IncomeForm(user=request.user)
        return render(request, "finances/form.html", {
            "form": form,
            "title": "Registrar ingreso",
        })

    def post(self, request):
        form = IncomeForm(request.POST, user=request.user)

        if not form.is_valid():
            return render(request, "finances/form.html", {
                "form": form,
                "title": "Registrar ingreso",
            })

        try:
            create_transaction(
                user=request.user,
                category=form.cleaned_data["category"],
                amount=form.cleaned_data["amount"],
                transaction_date=form.cleaned_data["transaction_date"],
                description=form.cleaned_data.get("description", ""),
            )
        except ValueError as e:
            form.add_error(None, str(e))
            return render(request, "finances/form.html", {
                "form": form,
                "title": "Registrar ingreso",
            })

        return redirect("finances:list")


class UpdateTransactionView(LoginRequiredMixin, View):
    def get(self, request, transaction_id):
        transaction = get_transaction(request.user, transaction_id)

        if transaction is None:
            return redirect("finances:list")

        form_cls = IncomeForm if transaction.category.is_income else ExpenseForm
        form = form_cls(instance=transaction, user=request.user)

        return render(request, "finances/form.html", {
            "form": form,
            "title": "Editar transacción",
        })

    def post(self, request, transaction_id):
        transaction = get_transaction(request.user, transaction_id)

        if transaction is None:
            return redirect("finances:list")

        form_cls = IncomeForm if transaction.category.is_income else ExpenseForm
        form = form_cls(request.POST, instance=transaction, user=request.user)

        if not form.is_valid():
            return render(request, "finances/form.html", {
                "form": form,
                "title": "Editar transacción",
            })

        try:
            update_transaction(
                transaction=transaction,
                category=form.cleaned_data["category"],
                amount=form.cleaned_data["amount"],
                transaction_date=form.cleaned_data["transaction_date"],
                description=form.cleaned_data.get("description", ""),
            )
        except ValueError as e:
            form.add_error(None, str(e))
            return render(request, "finances/form.html", {
                "form": form,
                "title": "Editar transacción",
            })

        return redirect("finances:list")


class DeleteTransactionView(LoginRequiredMixin, View):
    def post(self, request, transaction_id):
        transaction = get_transaction(request.user, transaction_id)

        if transaction is not None:
            delete_transaction(transaction)

        return redirect("finances:list")


#  Categories

class CategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        categories = get_categories(request.user)
        return render(request, "finances/categories/list.html", {
            "categories": categories,
        })


class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()
        return render(request, "finances/categories/form.html", {
            "form": form,
            "title": "Nueva categoría",
        })

    def post(self, request):
        form = CategoryForm(request.POST)

        if not form.is_valid():
            return render(request, "finances/categories/form.html", {
                "form": form,
                "title": "Nueva categoría",
            })

        try:
            create_category(
                user=request.user,
                name=form.cleaned_data["name"],
                category_type=form.cleaned_data["category_type"],
                icon=form.cleaned_data.get("icon", ""),
            )
        except ValueError as e:
            form.add_error(None, str(e))
            return render(request, "finances/categories/form.html", {
                "form": form,
                "title": "Nueva categoría",
            })

        return redirect("finances:category-list")


class UpdateCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = get_category(request.user, category_id)

        if category is None:
            return redirect("finances:category-list")

        form = CategoryForm(instance=category)
        return render(request, "finances/categories/form.html", {
            "form": form,
            "title": "Editar categoría",
        })

    def post(self, request, category_id):
        category = get_category(request.user, category_id)

        if category is None:
            return redirect("finances:category-list")

        form = CategoryForm(request.POST, instance=category)

        if not form.is_valid():
            return render(request, "finances/categories/form.html", {
                "form": form,
                "title": "Editar categoría",
            })

        try:
            update_category(
                category=category,
                name=form.cleaned_data["name"],
                category_type=form.cleaned_data["category_type"],
                icon=form.cleaned_data.get("icon", ""),
            )
        except ValueError as e:
            form.add_error(None, str(e))
            return render(request, "finances/categories/form.html", {
                "form": form,
                "title": "Editar categoría",
            })

        return redirect("finances:category-list")


class DeleteCategoryView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_category(request.user, category_id)

        if category is None:
            return redirect("finances:category-list")

        try:
            delete_category(category)
        except ValueError:
            return redirect("finances:category-list")

        return redirect("finances:category-list")