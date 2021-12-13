from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_main.urls")),
    path("", include("users_app.urls")),
]

handler404 = "app_main.views.http404_view"
