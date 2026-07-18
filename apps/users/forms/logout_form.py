from django import forms


class LogoutForm(forms.Form):
    confirm = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput,
        required=False,
    )
