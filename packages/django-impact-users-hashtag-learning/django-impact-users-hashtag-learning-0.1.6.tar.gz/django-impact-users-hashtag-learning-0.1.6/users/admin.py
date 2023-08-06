from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin

from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ImportExportModelAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {
        "fields": ("name", 'school', 'faculty', 'school_admin', 'show_overview_help', 'member_of_faculties')
    }),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", 'school',  "name", "is_superuser"]
    list_filter = ['school']
    search_fields = ["name", "username"]
