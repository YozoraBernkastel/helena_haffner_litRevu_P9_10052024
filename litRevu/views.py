from django.shortcuts import render, redirect
from . import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# class LoginPageView(View):
#     template_name = 'authentication/login.html'
#     form_class = forms.LoginForm
#
#     def get(self, request):
#         form = self.form_class()
#         message = ""
#         return render(request, self.template_name, context={"form": form, 'message': message})
#
#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#
#         if request.method == 'POST':
#             form = forms.LoginForm(request.POST)
#             if form.is_valid():
#                 user = authenticate(
#                     username=form.cleaned_data["username"],
#                     password=form.cleaned_data["password"],
#                 )
#                 if user is not None:
#                     login(request, user)
#                     return redirect("home")
#
#         message = "Identifiants invalides. Veuillez réessayer."
#         return render(request, self.template_name, context={'form': form, "message": message})

@login_required()
def home(request):
    return render(request, "litRevu/home.html")


class SignupPage(View):
    template_name = "authentication/signup.html"
    form = forms.SignupForm

    def get(self, request):
        form = forms.SignupForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if request.method == "POST":
            form = forms.SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, context={"form": form})


