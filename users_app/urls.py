from django.urls import path
from users_app.views import (
    register_view,
    logout_view,
    login_view,
    Password_Change_ClassView,
    Password_change_done_view,
)

urlpatterns = [
    path("kayit/", register_view, name="register"),
    path("cikis/", logout_view, name="logout"),
    path("giris/", login_view, name="login"),
    path(
        "sifre-degistir/", Password_Change_ClassView.as_view(), name="change_password"
    ),
    path(
        "sifre-degistir-basarili/",
        Password_change_done_view,
        name="password_change_done",
    ),
]
