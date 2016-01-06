"""Models for tuits app."""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Tuit(models.Model):
    """Model for tuit."""

    user = models.ForeignKey(User)
    message = models.TextField(blank=False, null=False)
    tuit_date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(
        upload_to='media/tuits/images',
        blank=True,
        null=True
    )
    video_file = models.FileField(
        upload_to='media/tuits/videos', max_length=200, blank=True, null=True
    )
    total_likes = models.IntegerField(default=0)
    total_retuits = models.IntegerField(default=0)

    is_retuit = models.BooleanField(default=False)
    original_tuit = models.ForeignKey(
        "Tuit",
        related_name='retuited_tuit',
        blank=True,
        null=True
    )

    def __str__(self):
        """Return tuit."""
        return "{user} tuited {message}...".format(
            user=self.user.username,
            message=self.message[:10]
        )


class UserLikesTuit(models.Model):
    """Model for user likes tuit."""

    user = models.ForeignKey(User, blank=False, null=False)
    tuit = models.ForeignKey(Tuit, blank=False, null=False)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return user likes tuit."""
        return "{user} liked tuit {message}...".format(
            user=self.user.username,
            message=self.tuit.message[:10]
        )
