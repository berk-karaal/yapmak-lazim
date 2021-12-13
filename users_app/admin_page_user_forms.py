from django import forms
from users_app.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Forms for admin page


class Admin_UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ("email", "name", "password1", "password2")

    # same clean_password2() method as UserCreationForm's, except Error message
    def clean_password2(self):
        # check if the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords empty or didn't match.")

        return password2

    # same save() method as UserCreationForm's
    def save(self, commit=True):
        # save the provided password in hashed format
        if self.is_valid():
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user


class Admin_UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("email", "password", "name", "is_active", "is_admin")
