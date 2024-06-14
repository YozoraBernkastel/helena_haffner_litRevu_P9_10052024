from django import forms
from django.urls import reverse_lazy

from litRevu.models import Ticket, Review


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
        success_url = reverse_lazy('home')


class ReviewCreationForm(forms.ModelForm):
    CHOICES = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    notes = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = Review
        fields = ("headline", "notes", "headline", "body")
