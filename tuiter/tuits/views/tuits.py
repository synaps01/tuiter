"""Teams Views module."""

from django.views import generic
from ..models import Tuit
from useraccounts.models import UserSettings, UserFollowsUser
from django.contrib.auth.models import User
from django.db.models import Q

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
        followed_users = UserFollowsUser.objects.filter(
                user=user
            )
        followed_users_ids = []
        for u in followed_users:
            followed_users_ids.append(u.followed_user.id)
        followed_users_ids.append(user.id)
        timeline_tuits = Tuit.objects.filter(
            user__in=followed_users_ids,
        ).order_by('-tuit_date')
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
        timeline_tuits = Tuit.objects.filter(
                user=user
            )
        ctxt = {
            'timeline_tuits': timeline_tuits,
            'user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers,
            'timeline_tuits': timeline_tuits
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
    if request.user.is_authenticated():
        user = request.user
        user_settings = UserSettings.objects.filter(
                user=user
            )[0]
        ctxt = {
            'user': user,
            'user_settings': user_settings
        }
        return render_to_response(
            'tuits/edit_profile.html',
            context=ctxt,
            context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
            )


def register(request):
    """Register function."""
    user = username = email = password = None
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        users = User.objects.filter(
                username=username
            )
        if users:
            dictionary = {'message': "Username already exists."}
            return render_to_response(
                'account/landing.html',
                context_instance=RequestContext(request)
            )
        else:
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            user_settings = UserSettings()
            user_settings.user = user
            user_settings.save()
            user_log_in = authenticate(
                username=username,
                password=password
                )
            if user_log_in is not None:
                if user_log_in.is_active:
                    login(request, user_log_in)
                    return HttpResponseRedirect(reverse('tuiter:timeline'))


def editBasicInfo(request):
    """Edit basic info function."""
    user = new_first_name = new_last_name = new_email = None
    if request.POST:
        new_first_name = request.POST['first_name']
        new_last_name = request.POST['last_name']
        new_email = request.POST['email']
        if request.user.is_authenticated():
            user = request.user
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email
            user.save()
            ctxt = {
                'userUpdated': 'yes'
            }
            return render_to_response(
                    'tuits/edit_profile.html',
                    context=ctxt,
                    context_instance=RequestContext(request)
                )
        else:
            return render_to_response(
                'account/landing.html',
                context_instance=RequestContext(request)
                )
    else:
        return render_to_response(
                'tuits/edit_profile.html',
                context_instance=RequestContext(request)
            )


def changePassword(request):
    """Change password function."""
    user = username = old_password = new_password = confirm_password = None
    if request.POST:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password != confirm_password:
            pass_message = 'The new password doesn\'t match'
            ctxt = {
                'pass_message': pass_message
            }
            return render_to_response(
                    'tuits/edit_profile.html',
                    context=ctxt,
                    context_instance=RequestContext(request)
                )
        elif request.user.is_authenticated():
            user = request.user
            username = request.user.username
            user_auth = authenticate(username=username, password=old_password)
            if user_auth is None:
                pass_message = 'The old password is incorrect'
                ctxt = {
                    'pass_message': pass_message
                }
                return render_to_response(
                        'tuits/edit_profile.html',
                        context=ctxt,
                        context_instance=RequestContext(request)
                    )
            else:
                user.set_password(new_password)
                user.save()
                new_user_session = authenticate(
                        username=username,
                        password=new_password
                    )
                if new_user_session is not None:
                    if new_user_session.is_active:
                        login(request, new_user_session)
                pass_message = 'Password updated successfully!'
                ctxt = {
                    'pass_message': pass_message
                }
                return render_to_response(
                        'tuits/edit_profile.html',
                        context=ctxt,
                        context_instance=RequestContext(request)
                    )
        else:
            return render_to_response(
                    'account/landing.html',
                    context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
                'tuits/edit_profile.html',
                context_instance=RequestContext(request)
            )


def searchUser(request):
    """search user function."""
    ctxt = None
    if request.POST:
        search_text = request.POST['search_text']
        users = User.objects.filter(
                Q(username__icontains=search_text) |
                Q(first_name__icontains=search_text) |
                Q(last_name__icontains=search_text)
            )
        ctxt = {
                'users': users
            }
    return render_to_response(
            'tuits/search_result.html',
            context=ctxt,
            context_instance=RequestContext(request)
        )


def userProfile(request, tuiter_username):
    """User profile function."""
    user = following_user = None
    user = request.user
    tuiter_users = tuiter_user = None
    tuiter_users = User.objects.filter(
        username=tuiter_username
        )
    if tuiter_users:
        tuiter_user = tuiter_users[0]
        if user:
            ufus = UserFollowsUser.objects.filter(
                    user=user,
                    followed_user=tuiter_user
                )
            if ufus:
                following_user = 'yes'
        user_settings = UserSettings.objects.filter(
                user=tuiter_user
            )[0]
        timeline_tuits = Tuit.objects.filter(
                user=tuiter_user
            )
        total_tuits = len(Tuit.objects.filter(
                user=tuiter_user
            ))
        total_following = len(UserFollowsUser.objects.filter(
                user=tuiter_user
            ))
        total_followers = len(UserFollowsUser.objects.filter(
                followed_user=tuiter_user
            ))
        timeline_tuits = Tuit.objects.filter(
                user=tuiter_user
            )
        ctxt = {
            'user': tuiter_user,
            'following_user': following_user,
            'source_user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers,
            'timeline_tuits': timeline_tuits
        }
        if user == tuiter_user:
            return render_to_response(
                    'tuits/my_profile.html',
                    context=ctxt,
                    context_instance=RequestContext(request)
                )
        else:
            return render_to_response(
                    'tuits/user_profile.html',
                    context=ctxt,
                    context_instance=RequestContext(request)
                )


def userFollow(request, tuiter_user):
    """User follow function."""
    if request.POST and request.user.is_authenticated:
        user = request.user
        ustf = User.objects.filter(
                username=tuiter_user
            )
        if ustf:
            user_to_follow = ustf[0]
            user_follows_user = None
            user_follows_user = UserFollowsUser.objects.filter(
                    user=user,
                    followed_user=user_to_follow
                )
            if not user_follows_user:
                user_follows_user = UserFollowsUser()
                user_follows_user.user = user
                user_follows_user.followed_user = user_to_follow
                user_follows_user.save()
                return HttpResponseRedirect(
                    reverse(
                        'tuiter:userProfile',
                        args=(user_to_follow.username,)
                        )
                    )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def userUnfollow(request, tuiter_user):
    """User unfollow function."""
    if request.POST and request.user.is_authenticated:
        user = request.user
        ustf = User.objects.filter(
                username=tuiter_user
            )
        if ustf:
            user_to_unfollow = ustf[0]
            user_follows_user = None
            user_follows_user = UserFollowsUser.objects.filter(
                    user=user,
                    followed_user=user_to_unfollow
                )
            if user_follows_user:
                ufu = user_follows_user[0]
                ufu.delete()
                return HttpResponseRedirect(
                    reverse(
                        'tuiter:userProfile',
                        args=(user_to_unfollow.username,)
                        )
                    )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def userProfileFollowing(request, tuiter_username):
    """Following users function."""
    user = following_user = None
    user = request.user
    tuiter_users = tuiter_user = None
    tuiter_users = User.objects.filter(
        username=tuiter_username
        )
    if tuiter_users:
        tuiter_user = tuiter_users[0]
        if user:
            ufus = UserFollowsUser.objects.filter(
                    user=user,
                    followed_user=tuiter_user
                )
            if ufus:
                following_user = 'yes'
        user_settings = UserSettings.objects.filter(
                user=tuiter_user
            )[0]
        timeline_tuits = Tuit.objects.filter(
                user=tuiter_user
            )
        total_tuits = len(Tuit.objects.filter(
                user=tuiter_user
            ))
        total_following = len(UserFollowsUser.objects.filter(
                user=tuiter_user
            ))
        total_followers = len(UserFollowsUser.objects.filter(
                followed_user=tuiter_user
            ))
        user_following_users = UserFollowsUser.objects.filter(
                user=tuiter_user
            )
        following_users_ids = []
        for u in user_following_users:
            following_users_ids.append(u.followed_user.id)
        following_users = User.objects.filter(
            id__in=following_users_ids,
        )
        ctxt = {
            'user': tuiter_user,
            'following_user': following_user,
            'source_user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers,
            'users': following_users
        }
        return render_to_response(
                'tuits/user_follows.html',
                context=ctxt,
                context_instance=RequestContext(request)
            )


def userProfileFollowers(request, tuiter_username):
    """Follower users function."""
    user = following_user = None
    user = request.user
    tuiter_users = tuiter_user = None
    tuiter_users = User.objects.filter(
        username=tuiter_username
        )
    if tuiter_users:
        tuiter_user = tuiter_users[0]
        if user:
            ufus = UserFollowsUser.objects.filter(
                    user=user,
                    followed_user=tuiter_user
                )
            if ufus:
                following_user = 'yes'
        user_settings = UserSettings.objects.filter(
                user=tuiter_user
            )[0]
        timeline_tuits = Tuit.objects.filter(
                user=tuiter_user
            )
        total_tuits = len(Tuit.objects.filter(
                user=tuiter_user
            ))
        total_following = len(UserFollowsUser.objects.filter(
                user=tuiter_user
            ))
        total_followers = len(UserFollowsUser.objects.filter(
                followed_user=tuiter_user
            ))
        user_follower_users = UserFollowsUser.objects.filter(
                followed_user=tuiter_user
            )
        follower_users_ids = []
        for u in user_follower_users:
            follower_users_ids.append(u.user.id)
        follower_users = User.objects.filter(
            id__in=follower_users_ids,
        )
        ctxt = {
            'user': tuiter_user,
            'following_user': following_user,
            'source_user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers,
            'users': follower_users
        }
        return render_to_response(
                'tuits/user_followers.html',
                context=ctxt,
                context_instance=RequestContext(request)
            )
