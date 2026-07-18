from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está registrado."
            )

        return email
