from django import forms

from apps.cycles.models import DailyLog, SymptomCategory


class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = [
            "energy_level",
            "mood",
            "symptoms",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["energy_level"].widget.attrs["class"] = "w-full"
        self.fields["mood"].widget.attrs["class"] = "w-full"

        self.symptom_categories = (
            SymptomCategory.objects
            .prefetch_related("symptoms")
            .all()
        )

        self.selected_symptoms = (
            set(
                self.instance.symptoms.values_list(
                    "id",
                    flat=True,
                )
            )
            if self.instance.pk
            else set()
        )