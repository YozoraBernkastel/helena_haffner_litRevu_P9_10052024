from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from authentication import views

urlpatterns = [
    path("signup", views.SignupPage.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),

]
