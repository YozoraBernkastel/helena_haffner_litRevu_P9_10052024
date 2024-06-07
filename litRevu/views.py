from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect
import litRevu.forms
from litRevu.forms import TicketCreationForm, TicketReviewCreationForm, ReviewCreationForm
from django.utils.decorators import method_decorator


@login_required()
def home(request):
    return render(request, "litRevu/home.html")


@method_decorator(login_required, name='dispatch')
class TicketCreationView(CreateView):
    template_name = "litRevu/creation/ticket.html"
    form_class = TicketCreationForm


@method_decorator(login_required, name='dispatch')
class TicketReviewCreationView(View):
    template_name = "litRevu/creation/ticket&review.html"
    form = litRevu.forms.TicketReviewCreationForm
    form2 = litRevu.forms.TicketCreationForm

    def get(self, request):
        form = litRevu.forms.TicketReviewCreationForm()
        form2 = litRevu.forms.TicketCreationForm()
        return render(request, self.template_name, context={"form": form, "form2": form2})

    def post(self, request):
        form = litRevu.forms.TicketReviewCreationForm(request.POST)
        if request.method == "POST":
            form = litRevu.forms.TicketReviewCreationForm(request.POST)
            # il faudra d'abord enregistrer le ticket, puis récupérer son id et enfin enregistrer la review
            if form.is_valid():
                form.save()
                return redirect("home")

        return render(request, self.template_name, context={"form": form})


@method_decorator(login_required, name='dispatch')
class ReviewCreationView(CreateView):
    # ressemble à TicketReviewCreationView mais la partie correspondant au ticket
    # doit afficher les infos du ticket sélectionner et donc il ne faut envoyer que les données
    # de la review à la base de données (peut-être plus simple que TicketReview pour commencer)
    # Il faudra surement hériter d'une autre classe
    template_name = "litRevu/creation/review.html"
    form_class = litRevu.forms.ReviewCreationForm




