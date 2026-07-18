from django import forms

from apps.users.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_email = self.instance.email if self.instance.pk else None

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if email != self._original_email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está registrado."
            )

        return email
