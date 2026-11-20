from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.forms import SignupForm
from gestione.models import *

# Create your views here.

def about(request):
    return render(request, template_name="about.html")


def vue_index(request):
    return render(request, template_name="index_vue.html")

class myLogin(auth_views.LoginView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            if self.request.session["show_signup"] == True:
                self.request.session["show_signup"] = False
                context["message"] = "User create with success!"
        except KeyError:
            print("Error!")
        return context

    def get_success_url(self):
        self.request.session["show_login"] = True
        success_url = reverse_lazy("index")
        return success_url


class signUp(CreateView):
    form_class = SignupForm
    template_name = "signup.html"

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        self.request.session["show_signup"] = True
        success_url = reverse_lazy("login")
        return success_url

@login_required
def myLogout(request):
    logout(request)
    return redirect('/?logout=ok')

