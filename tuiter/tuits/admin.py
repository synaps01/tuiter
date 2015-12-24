"""Admin for tuits."""

from django.contrib import admin
from .models import Tuit, UserLikesTuit


@admin.register(Tuit)
class TuitAdmin(admin.ModelAdmin):
    """Tuit Admin."""

    list_display = ('user', 'message')


@admin.register(UserLikesTuit)
class UserLikesTuitAdmin(admin.ModelAdmin):
    """Tuit Admin."""

    list_display = ('user', 'tuit', 'like_date')
