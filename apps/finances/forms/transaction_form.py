from datetime import date

from django import forms
from django.db.models import Q

from apps.finances.choices import CategoryType
from apps.finances.models import Category, Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            "category",
            "amount",
            "transaction_date",
            "description",
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["category"].queryset = Category.objects.filter(
                category_type=CategoryType.EXPENSE,
            ).filter(
                Q(user=user) | Q(user__isnull=True)
            )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "El monto debe ser mayor que cero."
            )

        return amount

    def clean_transaction_date(self):
        transaction_date = self.cleaned_data["transaction_date"]

        if transaction_date > date.today():
            raise forms.ValidationError(
                "La fecha no puede ser futura."
            )

        return transaction_date