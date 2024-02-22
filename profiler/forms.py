from django import forms
from .models import (
    CyberCriminal,
)
from .widgets import DatePickerInput


class CyberCriminalForm(forms.ModelForm):
    class Meta:
        model = CyberCriminal
        fields = [
            "name",
            "d_o_b",
            "nationality",
            "last_known_location",
            "hacker_classification",
            "height",
            "weight",
            "hair_color",
            "eye_color",
            "aggression_level",
            "risk_taking_level",
        ]
        widgets = {
            "d_o_b": DatePickerInput(),
            "aggression_level": forms.NumberInput(
                attrs={"type": "range", "min": 1, "max": 10, "step": 1, "value": 5}
            ),
            "risk_taking_level": forms.NumberInput(
                attrs={"type": "range", "min": 1, "max": 10, "step": 1, "value": 5}
            ),
        }
        labels = {
            "d_o_b": "Date of Birth",
            "name": "Full Name",
            "aggression_level": "Level of Aggression",
            "risk_taking_level": "Level of Risk Taken",
        }
