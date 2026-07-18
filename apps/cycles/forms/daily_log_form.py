from django import forms

from apps.cycles.models import DailyLog


class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = [
            "energy_level",
            "mood",
            "symptoms",
            "notes",
        ]