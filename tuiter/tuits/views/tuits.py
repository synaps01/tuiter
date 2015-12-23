"""Teams Views module."""

from django.views import generic

from django.views.generic import (
    TemplateView,
)

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def landingPageView(request):
    """function for landing view."""
    return render_to_response(
        'account/landing.html',
        context_instance=RequestContext(request)
        )


def tuiter_login(request):
    """login function."""
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('tuiter:timeline'))
    dictionary = {'message': "Wrong username or password"}
    return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def timeline(request):
    """timeline function."""
    return HttpResponse("you are on the timeline")
