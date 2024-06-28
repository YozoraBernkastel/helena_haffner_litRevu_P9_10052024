from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import User
from litRevu.forms import TicketCreationForm, ReviewCreationForm, SubscribeCreationForm
from django.utils.decorators import method_decorator
from litRevu.models import Ticket, UserFollows


@login_required()
def home(request):
    tickets = Ticket.objects.all()
    return render(request, "litRevu/home.html", {"tickets": tickets})


@method_decorator(login_required, name='dispatch')
class SubCreationView(CreateView):
    template_name = "litRevu/subscribe.html"
    form_class = SubscribeCreationForm

    def get(self, request, *args, **kwargs):
        subs = UserFollows.objects.filter(user=self.request.user)
        followers = UserFollows.objects.filter(followed_user=self.request.user)
        users_list = User.objects.all()
        context = {"users": users_list, "subs": subs, "followers": followers, "error_message": ""}

        return render(request, self.template_name, context)


def sub_to(request):
    follow = request.POST.get("followed_user")
    try:
        user_to_follow = User.objects.get(username=follow)
        sub_to_user = UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
        sub_to_user.save()
        subs = UserFollows.objects.filter(user=request.user)

        return render(request, 'litRevu/subscriptions_table.html', {'subs': subs})
    except User.DoesNotExist:
        print("erreur blabla")
        error_message = f"L'utilisateur {follow} n'existe pas."
        subs = UserFollows.objects.filter(user=request.user)
        return render(request, 'litRevu/subscriptions_table.html', {"subs": subs, "error_message": error_message})


def unsub_to(request, unfollow_user):
    user_to_unfollow = User.objects.get(username=unfollow_user)
    follow_obj = UserFollows.objects.get(user=request.user, followed_user=user_to_unfollow)

    if follow_obj:
        follow_obj.delete()
        subs = UserFollows.objects.filter(user=request.user)
        return render(request, 'litRevu/subscriptions_table.html', {'subs': subs})


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
        form.instance.ticket = self.ticket

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
