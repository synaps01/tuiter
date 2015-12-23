"""Urls for tuits."""

from django.conf.urls import url

from .views import tuits

urlpatterns = [
    url(r'^$', tuits.landingPageView, name='landing'),
    url(r'login$', tuits.tuiter_login, name='login'),
    url(r'timeline$', tuits.timeline, name='timeline')
]
