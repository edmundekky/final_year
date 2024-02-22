from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Investigator, Contact


class InvestigatorForm(UserCreationForm):
    class Meta:
        model = Investigator
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "password1",
            "password2",
            "username",
        )


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("subject", "message")
