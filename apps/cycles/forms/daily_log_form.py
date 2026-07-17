from django import forms

from apps.cycles.models.daily_log import DailyLog


class LogDayForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = [
            "energy_level",
            "mood",
            "symptoms",
            "notes",
        ]