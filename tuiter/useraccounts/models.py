"""Models for useraccounts app."""

from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.db import models


class UserSettings(models.Model):
    """Model for user settings."""

    user = models.OneToOneField(User)
    profile_picture = models.ImageField(
        upload_to='media/users/profile_pictures',
        blank=True,
        null=True
    )
    cover_picture = models.ImageField(
        upload_to='media/users/profile_pictures',
        blank=True,
        null=True
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        """Return full name."""
        return "{name} settings".format(
            name=self.user.username
        )


class UserFollowsUser(models.Model):
    """Model for user settings."""

    user = models.ForeignKey(User, related_name='user')
    followed_user = models.ForeignKey(User, related_name='followed_user')
    follow_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return user follows."""
        return "{name} follows {followed}".format(
            name=self.user.username,
            followed=self.followed_user.username
        )
