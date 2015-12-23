"""Admin for tuits."""

from django.contrib import admin
from .models import Tuit


@admin.register(Tuit)
class TuitAdmin(admin.ModelAdmin):
    """Tuit Admin."""

    list_display = ('user', 'message')
