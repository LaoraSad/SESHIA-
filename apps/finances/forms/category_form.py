from django import forms

from apps.finances.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "category_type",
            "icon",
        ]

    def clean_name(self):
        return self.cleaned_data["name"].strip()