"""Teams Views module."""

from django.views import generic
from ..models import Tuit
from useraccounts.models import UserSettings, UserFollowsUser

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


def tuiter_logout(request):
    """logout funciton."""
    logout(request)
    return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def timeline(request):
    """timeline function."""
    ctxt = None
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
    else:
        return render_to_response(
            'account/landing.html',
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


def my_profile(request):
    """my_profile funciton."""
    if request.user.is_authenticated():
        user = request.user
        user_settings = UserSettings.objects.filter(
                user=user
            )[0]
        timeline_tuits = Tuit.objects.filter(
                user=user,
            )
        total_tuits = len(Tuit.objects.filter(
                user=user
            ))
        total_following = len(UserFollowsUser.objects.filter(
                user=user
            ))
        total_followers = len(UserFollowsUser.objects.filter(
                followed_user=user
            ))
        ctxt = {
            'timeline_tuits': timeline_tuits,
            'user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers
        }
        return render_to_response(
            'tuits/my_profile.html',
            context=ctxt,
            context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
            )


def edit_profile(request):
    """Edit profile function."""
    return HttpResponse("editing profile ...")
