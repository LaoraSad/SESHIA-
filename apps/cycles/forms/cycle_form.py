from django import forms
from datetime import date

from apps.cycles.models.cycle import Cycle


class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = [
            "start_date",
            "expected_length",
            "notes",
        ]

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]

        if start_date > date.today():
            raise forms.ValidationError(
                "La fecha de inicio no puede ser futura."
            )

        return start_date