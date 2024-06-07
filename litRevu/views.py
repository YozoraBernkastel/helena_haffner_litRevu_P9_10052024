from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect
import litRevu.forms
from litRevu.forms import TicketCreationForm, TicketReviewCreationForm
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
    template_name = "litRevu/creation/review.html"
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
            if form.is_valid():
                form.save()
                return redirect("home")

        return render(request, self.template_name, context={"form": form})


class ReviewCreationView(TicketReviewCreationForm):
    template_name = "blabla"




