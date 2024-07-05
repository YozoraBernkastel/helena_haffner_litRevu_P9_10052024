from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import User
from litRevu.forms import TicketCreationForm, ReviewCreationForm, SubscribeCreationForm
from django.utils.decorators import method_decorator
from litRevu.models import Ticket, Review, UserFollows


@login_required()
def flux(request):
    # todo il faudra faire en sorte de ne récupérer que les tickets des personnes suivies (et de l'utilisateur ?)
    tickets = Ticket.objects.all()
    return render(request, "litRevu/flux.html", {"tickets": tickets, "flux": True})


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


@login_required()
def sub_to(request):
    template: str = 'litRevu/_subscriptions_table.html'
    follow = request.POST.get("followed_user")
    try:
        user_to_follow = User.objects.get(username=follow)
        same_user = user_to_follow == request.user
        already_sub = len(UserFollows.objects.filter(user=request.user, followed_user=user_to_follow)) > 0

        if same_user:
            error_message = f"Vous ne pouvez pas vous suivre vous-même."
        elif already_sub:
            error_message = f"Vous suivez déjà {follow}."
        else:
            sub_to_user = UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            sub_to_user.save()
            error_message = False

        subs = UserFollows.objects.filter(user=request.user)
        return render(request, template, {"subs": subs, "error_message": error_message})

    except User.DoesNotExist:
        error_message = f"L'utilisateur {follow} n'existe pas."
        subs = UserFollows.objects.filter(user=request.user)
        return render(request, template, {"subs": subs, "error_message": error_message})


@login_required()
def unsub_to(request, unfollow_user):
    user_to_unfollow = User.objects.get(username=unfollow_user)
    follow_obj = UserFollows.objects.get(user=request.user, followed_user=user_to_unfollow)

    if follow_obj:
        follow_obj.delete()
        subs = UserFollows.objects.filter(user=request.user)
        return render(request, 'litRevu/_subscriptions_table.html', {'subs': subs})


@method_decorator(login_required, name='dispatch')
class TicketCreationView(CreateView):
    template_name = "litRevu/creation/_ticket.html"
    form_class = TicketCreationForm
    success_url = reverse_lazy("flux")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ReviewCreationView(CreateView):
    template_name = "litRevu/creation/review.html"
    form_class = ReviewCreationForm
    success_url = reverse_lazy("flux")
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
        kwargs["content"] = self.ticket
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
    success_url = reverse_lazy("flux")

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

                return redirect("flux")

        return render(request, self.template_name, context={"form": ticket_form, "form2": review_form})


@method_decorator(login_required, name='dispatch')
class UserPostsView(View):
    template = "litRevu/user_posts.html"

    def get(self, request):
        user_tickets = Ticket.objects.filter(user=request.user)
        user_reviews = Review.objects.filter(user=request.user)
        # todo assembler et trier les tickets et reviews ici ? Sinon envoyer les deux et créer un onglet pour
        #  chaque afin que ce soit plus pratique pour l'utilisateur.
        #  Dans ce cas on pourrait passer d'un onglet à l'autre sans refresh grâce à HTMX, non ?
        #  Si j'opte pour cette solution, il faudra penser à renommer "content" dans le html "ticket" (voir ticket_content.html, flux et user_posts.html)
        user_posts = user_tickets
        content_exists = len(user_posts) > 0

        return render(request, self.template, context={"content_exists": content_exists, "posts": user_posts})
