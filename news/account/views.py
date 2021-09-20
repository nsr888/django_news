from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy


def user_login(request):
    if request.is_ajax and request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = user = authenticate(username=username, password=password)
            print("form valid")
            if user:
                login(request, user)
                return JsonResponse(
                    {"success": True, "message": "Logged as " + user.username}
                )
        print("Errors: ", login_form.errors)
        return JsonResponse({"success": False, "message": "Form not valid!"})
    else:
        login_form = AuthenticationForm()
    return render(request, "login.html", {"form": login_form})


def user_logout(request):
    logout(request)
    return JsonResponse({"success": True})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("acc")
