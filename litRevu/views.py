from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect
import litRevu.forms
from litRevu.forms import TicketCreationForm, ReviewCreationForm
from django.utils.decorators import method_decorator
from litRevu.models import Ticket, Review


@login_required()
def home(request):
    return render(request, "litRevu/home.html")


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
    # ressemble à TicketReviewCreationView mais la partie correspondant au ticket
    # doit afficher les infos du ticket sélectionner et donc il ne faut envoyer que les données
    # de la review à la base de données (peut-être plus simple que TicketReview pour commencer)
    # Il faudra surement hériter d'une autre classe
    template_name = "litRevu/creation/review.html"
    form_class = ReviewCreationForm

    def is_valid(self, form):
        form.instance.user = self.request.user
        form.instance.rating = self.request.notes
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form = ReviewCreationForm()
        # self.request.title.
        pass

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ReviewCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                return render(request, self.template_name, context={"form": form})


@method_decorator(login_required, name='dispatch')
class TicketReviewCreationView(View):
    template_name = "litRevu/creation/ticket&review.html"
    form = ReviewCreationForm
    form2 = TicketCreationForm

    def get(self, request):
        form = ReviewCreationForm()
        form2 = TicketCreationForm()
        return render(request, self.template_name, context={"form": form, "form2": form2})

    def post(self, request):
        # todo création d'un ticket / review.objects.create( dedans tu utilise cleaned_data pour récupérer chaque infos dans
        #  form et tu les ajotues à l'objet et comem ça tu as les deux objets correspondant à la BDD)
        form = ReviewCreationForm(request.POST)
        if request.method == "POST":
            # form = ReviewCreationForm(request.POST)
            r = self.request
            Ticket.objects.create(user=r.user, title=r.title, description=r.description, image=r.image)
            Review.objects.create()
            # todo CLASSE EN CHANTIER !!!!
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                return render(request, self.template_name, context={"form": form})

        return render(request, self.template_name, context={"form": form})
