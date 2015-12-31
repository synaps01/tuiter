"""Teams Views module."""

from django.views import generic
from ..models import Tuit

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
    username = None
    if request.user.is_authenticated():
        user = request.user
        username = request.user.username
    timeline_tuits = Tuit.objects.filter(
            user=user,
        )
    ctxt = {
        'timeline_tuits': timeline_tuits,
        'username': username
    }
    return render_to_response(
        'tuits/timeline.html',
        context=ctxt,
        context_instance=RequestContext(request)
        )


def newtuit(request):
    """newtuit funciton."""
    tuit_text = ''
    if request.POST:
        tuit_text = request.POST['tuit_text']
    if tuit_text and len(tuit_text) > 0 and request.user.is_authenticated():
        user = request.user
        newT = Tuit()
        newT.user = user
        newT.message = tuit_text
        newT.save()
    return HttpResponseRedirect(reverse('tuiter:timeline'))
