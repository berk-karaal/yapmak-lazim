from django.shortcuts import redirect, render
from users_app.forms import Registration_Form, Login_Form, Password_Changing_Form
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, authenticate, logout
from django.urls.base import reverse_lazy


def register_view(request):
    user = request.user
    if user.is_authenticated:
        # user is already authenticated
        return redirect("welcome")

    if request.method == "POST":
        form = Registration_Form(request.POST)
        if form.is_valid():
            form.save()  # created (registered) new user with given form datas(answers)

            # auto login registered user
            email = form.cleaned_data["email"].lower()
            raw_password = form.cleaned_data["password1"]
            account = authenticate(email=email, password=raw_password)  # verify
            # don't need to check the result of verifying, we created that just now
            login(request, account)

            return redirect_next_if_exist(request) or redirect("welcome")

    else:
        form = Registration_Form()

    return render(request, "users_app/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("welcome")


def login_view(request):
    if request.user.is_authenticated:
        # user already logged in
        return redirect("welcome")

    if request.method == "POST":
        form = Login_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            raw_password = form.cleaned_data["password"]
            user = authenticate(
                email=email, password=raw_password
            )  # verify credentials
            if user:
                # verified successfully
                login(request, user)

                return redirect_next_if_exist(request) or redirect("welcome")
    else:
        form = Login_Form()

    return render(request, "users_app/login.html", {"form": form})


class Password_Change_ClassView(PasswordChangeView):
    form_class = Password_Changing_Form
    success_url = reverse_lazy("password_change_done")
    template_name = "users_app/password_change.html"


def Password_change_done_view(request):
    return render(request, "users_app/password_change_done.html")


def redirect_next_if_exist(request):
    if request.GET:
        if request.GET.get("next"):
            return redirect(str(request.GET.get("next")))

    return None
