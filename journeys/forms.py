from journeys.models import Journey
from django import forms
from django.contrib.auth.models import User


class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = ("starting_from", "going_to", "going_date", "going_time", "description")
