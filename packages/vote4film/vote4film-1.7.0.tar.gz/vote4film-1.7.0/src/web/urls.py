from django.contrib.auth.views import LoginView, logout_then_login
from django.urls import path
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "web/home.html"


class LoginView(LoginView):
    template_name = "web/login.html"


app_name = "web"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("logout/", logout_then_login, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
]
