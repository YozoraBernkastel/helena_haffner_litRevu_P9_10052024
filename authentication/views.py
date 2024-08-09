
from django.shortcuts import render, redirect
from . import forms
from django.conf import settings

from django.contrib.auth import login
from django.views.generic import View


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
