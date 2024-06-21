from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from litRevu.forms import TicketCreationForm, ReviewCreationForm
from django.utils.decorators import method_decorator
from litRevu.models import Ticket, Review


@login_required()
def home(request):
    tickets = Ticket.objects.all()
    return render(request, "litRevu/home.html", {"tickets": tickets})


@method_decorator(login_required, name='dispatch')
class TicketCreationView(CreateView):
    template_name = "litRevu/creation/ticket.html"
    form_class = TicketCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ReviewCreationView(CreateView):
    template_name = "litRevu/creation/review.html"
    form_class = ReviewCreationForm
    success_url = reverse_lazy("home")
    _ticket = None

    @property
    def ticket(self):
        """
            cache personalisé pour _ticket
        """
        if self._ticket is None:
            self._ticket = get_object_or_404(Ticket, pk=self.kwargs["id"])

        return self._ticket

    def get_context_data(self, **kwargs):
        kwargs["ticket"] = self.ticket
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.rating = form.cleaned_data["note"]
        form.instance.user = self.request.user
        # appelle la base de données pour récupérer le ticket -> permet de vérifier si le ticket existe ! (mais plus couteux)
        form.instance.ticket = self.ticket
        # mode moins couteux mais risqué car pas de vérification qu'un objet avec cet id existe
        # form.instance.ticket_id = self.kwargs["id"]

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TicketReviewCreationView(View):
    template_name = "litRevu/creation/ticket&review.html"
    ticket_form = TicketCreationForm
    review_form = ReviewCreationForm
    success_url = reverse_lazy("home")

    def get(self, request):
        ticket_form = TicketCreationForm()
        review_form = ReviewCreationForm()

        return render(request, self.template_name, context={"form": ticket_form, "form2": review_form})

    def post(self, request):
        if request.method == "POST":
            ticket_form = TicketCreationForm(request.POST)
            review_form = ReviewCreationForm(request.POST)

            ticket_form.instance.user = self.request.user

            if ticket_form.is_valid():
                ticket = ticket_form.save()

                if review_form.is_valid():
                    review_form.instance.ticket_id = ticket.id
                    review_form.instance.rating = review_form.cleaned_data["note"]
                    review_form.instance.user = self.request.user
                    review_form.save()

                    return redirect("home")

            return render(request, self.template_name, context={"form": ticket_form, "form2": review_form})
