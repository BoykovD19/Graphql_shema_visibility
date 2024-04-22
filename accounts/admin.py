from django.contrib import admin

from accounts.models import User, UserInfo


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
    ]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "test_data"
    ]
