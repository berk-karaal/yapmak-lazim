from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate

from users_app.models import CustomUser


class Registration_Form(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        label="Email",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Email adresiniz",
            }
        ),  # don't need to set autofocus attr, it is built-in for USERNAME_FIELD
        required=True,
    )
    name = forms.CharField(
        max_length=100,
        label="İsim",
        widget=forms.TextInput(
            attrs={"autocomplete": "name", "placeholder": "İsminiz"}
        ),
        required=True,
    )

    # password1 and 2 are already declared in UserCreationForm
    # I am overwriting these in order to add placeholder
    password1 = forms.CharField(
        label="Şifre",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Şifre"}
        ),
    )
    password2 = forms.CharField(
        label="Şifrenizi onaylayın",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Şifre (tekrar)"}
        ),
    )

    error_messages = {
        "password_mismatch": "Girilen iki şifre aynı değil.",
    }

    class Meta:
        model = CustomUser
        fields = ("email", "name", "password1", "password2")

    # NOTE: clean_<field_name> methods are normally executed when you call the is_valid() method on a form
    #
    # check if email is already registered
    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        try:
            CustomUser.objects.get(email=email)
        except Exception as e:
            # this mail is not used, it is safe to use
            return email

        raise forms.ValidationError(f"{email} adresi zaten kullanılıyor.")

    # this method is not necessary, just for an example
    # aim: Do not accept names which is shorter than 4 characters
    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise forms.ValidationError("İsminiz en az 3 karakter olmalı.")

        return name


class Login_Form(forms.ModelForm):
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Email adresiniz",
                "autofocus": "",
            }
        ),
    )
    password = forms.CharField(
        label="Şifre",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "placeholder": "Şifreniz"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password")

    # we need to overwrite this function because we will use ModelForm for our custom purposes
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]

            # authenticate() returns None if failed
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Hatalı email ya da şifre.")


class Password_Changing_Form(PasswordChangeForm):
    old_password = forms.CharField(
        label="Eski şifreniz",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Şu anda kullandığınız şifre",
                "autofocus": "",
            }
        ),
    )

    new_password1 = forms.CharField(
        label="Yeni şifre",
        widget=forms.PasswordInput(attrs={"autocomplete": "Yeni şifreniz"}),
    )
    new_password2 = forms.CharField(
        label="Yeni şifrenizi onaylayın",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Yeni şifreniz (tekrar)",
            }
        ),
    )

    error_messages = {
        "password_mismatch": "Girilen iki şifre aynı değil.",
        "password_incorrect": "Eski şifreniz yanlış. Lütfen tekrar giriniz.",
    }

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password1", "new_password2"]
