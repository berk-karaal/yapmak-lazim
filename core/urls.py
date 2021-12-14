from django.contrib import admin
from django.urls import path, include
import os

urlpatterns = [
    path(f"{os.environ.get('ADMIN_PAGE_PATH')}/", admin.site.urls),
    path("", include("app_main.urls")),
    path("", include("users_app.urls")),
]

handler404 = "app_main.views.http404_view"
