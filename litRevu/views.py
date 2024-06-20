from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect
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

    def is_valid(self, form):
        form.instance.user = self.request.user
        form.instance.rating = self.request.notes
        return super().form_valid(form)

    def get(self, request, id):
        form = ReviewCreationForm()
        ticket = Ticket.objects.get(pk=id)
        return render(request, self.template_name, context={"form": form, "ticket": ticket})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ReviewCreationForm(request.POST)
            print(self.request)
            Review.objects.create(user=self.request.user, rating=request.POST.get("note"), ticket_id=request.POST.get("ticket_id"))
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
        # todo Créer un CreationForm unique dans lequel on fusionne review et ticket afin de faciliter les choses à l'envoi ?
        # todo Peut-être tester avant, histoire de voir si on peut les trouver dans request.cleaned_data
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
