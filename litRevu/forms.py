from django import forms
from django.urls import reverse_lazy

from litRevu.models import Ticket, Review, UserFollows


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("id", "title", "author", "description", "image")
        success_url = reverse_lazy('flux')


class ReviewCreationForm(forms.ModelForm):
    CHOICES = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    note = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    # todo réécrire le init et définir dedans le widget de rating

    class Meta:
        model = Review
        fields = ("headline", "note", "body")


class SubscribeCreationForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ("followed_user",)
