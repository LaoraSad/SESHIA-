from datetime import date

from django import forms

from apps.base.services.date_service import get_current_date
from apps.cycles.models import Cycle


class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = [
            "start_date",
            "expected_length",
            "notes",
        ]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"},
            ),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]
        simulated = get_current_date()

        if simulated == date.today() and start_date > simulated:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser futura."
            )

        return start_date