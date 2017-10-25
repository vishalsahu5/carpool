from journeys.models import Journey
from django import forms


class JourneyForm(forms.ModelForm):
    starting_from = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': "startingFromTextField"}))
    going_to = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': "goingToTextField"}))
    going_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Journey
        fields = ("starting_from", "going_to", "going_date", "going_time", "description")


class SearchJourneyForm(forms.ModelForm):
    starting_from = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': "startingFromTextField"}))
    going_to = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': "goingToTextField"}))

    class Meta:
        model = Journey
        fields = ("starting_from", "going_to")
