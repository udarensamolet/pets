from django.contrib import admin

from petstagram.accounts.models import PetstagramUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


admin.site.register(PetstagramUser, ProfileAdmin)
