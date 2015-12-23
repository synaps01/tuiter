"""Admin for useraccounts."""

from django.contrib import admin
from .models import UserSettings, UserFollowsUser


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    """UserSettingsAdmin."""

    list_display = ('user',)


@admin.register(UserFollowsUser)
class UserFollowsUserAdmin(admin.ModelAdmin):
    """UserFollowsUser Admin."""

    list_display = ('user', 'followed_user')
