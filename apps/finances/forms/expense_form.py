from datetime import date

from django import forms

from apps.base.services.date_service import get_current_date
from apps.finances.choices import CategoryType
from apps.finances.models import Transaction
from apps.finances.services.category_service import get_categories


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "category",
            "amount",
            "transaction_date",
            "description",
        ]
        widgets = {
            "transaction_date": forms.DateInput(
                attrs={"type": "date"},
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is None:
            raise TypeError("ExpenseForm requiere el argumento 'user'.")

        if user:
            self.fields["category"].queryset = (
                get_categories(user).filter(
                    category_type=CategoryType.EXPENSE,
                )
            )

        self.fields["category"].label_from_instance = (
            lambda obj: f"{obj.icon} {obj.name}"
        )

    def clean_transaction_date(self):
        transaction_date = self.cleaned_data["transaction_date"]
        simulated = get_current_date()

        if simulated == date.today():
            if transaction_date > simulated:
                raise forms.ValidationError(
                    "La fecha no puede ser futura."
                )

        return transaction_date