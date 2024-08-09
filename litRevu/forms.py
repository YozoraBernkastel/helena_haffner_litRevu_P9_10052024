from django import forms
from django.urls import reverse_lazy

from litRevu.models import Ticket, Review, UserFollows


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("id", "title", "author", "description", "image")
        success_url = reverse_lazy('flux')


class ReviewCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
        self.fields["rating"].widget = forms.RadioSelect(choices=choices)
        self.fields["rating"].label = "note"

    class Meta:
        model = Review
        fields = ("headline", "rating", "body")


class SubscribeCreationForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ("followed_user",)

