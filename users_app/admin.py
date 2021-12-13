from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users_app.models import CustomUser
from users_app.admin_page_user_forms import Admin_UserCreationForm, Admin_UserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = Admin_UserCreationForm
    form = Admin_UserChangeForm

    # things to show on list that all users listed
    list_display = ("email", "name", "is_admin")
    list_filter = ("is_admin",)

    # because of register_date is non-editable field, we must specify that
    readonly_fields = ("register_date",)

    # when you click on user from list
    fieldsets = (
        (
            "General",
            {"fields": ("email", "password", "register_date")},
        ),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_admin")}),
    )

    # add new user page's fields
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )

    search_fields = ("email", "name")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)

# unregister the Group model from admin panel
admin.site.unregister(Group)
