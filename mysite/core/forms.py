from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Simulations

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )

class GenerateSimulationForm(forms.ModelForm):
    class Meta:
        model = Simulations
        fields = ['name', 'cirfile']
