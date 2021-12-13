from django.contrib import admin
from django.contrib.admin import ModelAdmin
from app_main.models import Todo


class Todo_Admin(ModelAdmin):
    model = Todo

    readonly_fields = ("update_date",)

    list_display = ("__str__", "owner")


admin.site.register(Todo, Todo_Admin)
