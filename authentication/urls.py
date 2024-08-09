from django.urls import path
from django.contrib.auth.views import LogoutView
from authentication import views

urlpatterns = [
    path("signup", views.SignupPage.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),

]
