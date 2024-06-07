from django import forms
from django.urls import reverse_lazy

from litRevu.models import Ticket, Review


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
        success_url = reverse_lazy('home')


class TicketReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "headline", "body", "user")


# class ReviewCreationForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ("ticket", "rating", "headline", "body", "user")
