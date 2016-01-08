"""Teams Views module."""

from django.views import generic
from ..models import Tuit, UserLikesTuit
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
import json
import ast


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
        user_likes_tuits = UserLikesTuit.objects.filter(user=user)
        tuits = []
        for t in timeline_tuits:
            tuit_data = {
                'tuit_object': t,
                'liked': False
            }
            for ult in user_likes_tuits:
                if t == ult.tuit:
                    tuit_data['liked'] = True
                    break
            tuits.append(tuit_data)
        redirect_url = 'tuiter:timeline'
        ctxt = {
            'timeline_tuits': tuits,
            'username': username,
            'logged_user': user,
            'redirect_url': redirect_url,
            'use_parameters': False
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
            ).order_by('-tuit_date')
        total_tuits = len(Tuit.objects.filter(
                user=user
            ))
        total_following = len(UserFollowsUser.objects.filter(
                user=user
            ))
        total_followers = len(UserFollowsUser.objects.filter(
                followed_user=user
            ))
        user_likes_tuits = UserLikesTuit.objects.filter(user=user)
        tuits = []
        for t in timeline_tuits:
            tuit_data = {
                'tuit_object': t,
                'liked': False
            }
            for ult in user_likes_tuits:
                if t == ult.tuit:
                    tuit_data['liked'] = True
                    break
            tuits.append(tuit_data)
        redirect_url = 'tuiter:userProfile'
        ctxt = {
            'timeline_tuits': tuits,
            'user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers,
            'logged_user': user,
            'redirect_url': redirect_url,
            'use_parameters': True,
            'parameter_value': user.username
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
            user_settings = UserSettings.objects.get(user=user)
            ctxt = {
                'userUpdated': 'yes',
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
            user = request.user
            user_settings = UserSettings.objects.get(user=user)
            ctxt = {
                'pass_message': pass_message,
                'user': user,
                'user_settings': user_settings
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
                pass_message = 'The old password is not correct'
                user_settings = UserSettings.objects.get(user=user)
                ctxt = {
                    'pass_message': pass_message,
                    'user': user,
                    'user_settings': user_settings
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
                user_settings = UserSettings.objects.get(user=new_user_session)
                ctxt = {
                    'pass_message': pass_message,
                    'user': new_user_session,
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
            ).order_by('-tuit_date')
        total_tuits = len(Tuit.objects.filter(
                user=tuiter_user
            ))
        total_following = len(UserFollowsUser.objects.filter(
                user=tuiter_user
            ))
        total_followers = len(UserFollowsUser.objects.filter(
                followed_user=tuiter_user
            ))
        user_likes_tuits = UserLikesTuit.objects.filter(user=user)
        tuits = []
        for t in timeline_tuits:
            tuit_data = {
                'tuit_object': t,
                'liked': False
            }
            for ult in user_likes_tuits:
                if t == ult.tuit:
                    tuit_data['liked'] = True
                    break
            tuits.append(tuit_data)
        redirect_url = 'tuiter:userProfile'
        ctxt = {
            'user': tuiter_user,
            'following_user': following_user,
            'source_user': user,
            'user_settings': user_settings,
            'total_tuits': total_tuits,
            'total_following': total_following,
            'total_followers': total_followers,
            'timeline_tuits': tuits,
            'logged_user': user,
            'redirect_url': redirect_url,
            'use_parameters': True,
            'parameter_value': tuiter_username
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
            'users': following_users,
            'logged_user': user
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
            'users': follower_users,
            'logged_user': user
        }
        return render_to_response(
                'tuits/user_followers.html',
                context=ctxt,
                context_instance=RequestContext(request)
            )


def deleteTuit(request):
    """Delete tuit function."""
    if request.POST and request.user.is_authenticated:
        tuit_id = request.POST['tuit_id']
        redirect_url = request.POST['redirect_url']
        use_parameters = request.POST['use_parameters']
        user = request.user
        tuit = Tuit.objects.get(pk=tuit_id)
        if tuit.user == user:
            tuit.delete()
        if use_parameters == 'True':
            parameter_value = request.POST['parameter_value']
            return HttpResponseRedirect(
                    reverse(
                        redirect_url,
                        kwargs={
                            'tuiter_username': parameter_value
                        }
                    )
                )
        else:
            return HttpResponseRedirect(
                    reverse(redirect_url)
                )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def likeTuit(request):
    """Like tuit function."""
    if request.POST and request.user.is_authenticated:
        tuit_id = request.POST['tuit_id']
        redirect_url = request.POST['redirect_url']
        use_parameters = request.POST['use_parameters']
        user = request.user
        tuit = Tuit.objects.get(pk=tuit_id)
        user_likes_tuits = None
        user_likes_tuits = UserLikesTuit.objects.filter(
                user=user,
                tuit=tuit
            )
        if not user_likes_tuits:
            user_likes_tuit = UserLikesTuit()
            user_likes_tuit.user = user
            user_likes_tuit.tuit = tuit
            user_likes_tuit.save()
            tuit.total_likes = tuit.total_likes+1
            tuit.save()
        if use_parameters == 'True':
            parameter_value = request.POST['parameter_value']
            return HttpResponseRedirect(
                    reverse(
                        redirect_url,
                        kwargs={
                            'tuiter_username': parameter_value
                        }
                    )
                )
        else:
            return HttpResponseRedirect(
                    reverse(redirect_url)
                )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def removeTuitLike(request):
    """Dislike tuit function."""
    if request.POST and request.user.is_authenticated:
        tuit_id = request.POST['tuit_id']
        redirect_url = request.POST['redirect_url']
        use_parameters = request.POST['use_parameters']
        user = request.user
        tuit = Tuit.objects.get(pk=tuit_id)
        user_likes_tuits = None
        user_likes_tuits = UserLikesTuit.objects.filter(
                user=user,
                tuit=tuit
            )
        if user_likes_tuits:
            user_likes_tuit = user_likes_tuits[0]
            user_likes_tuit.delete()
            tuit.total_likes = tuit.total_likes-1
            tuit.save()
        if use_parameters == 'True':
            parameter_value = request.POST['parameter_value']
            return HttpResponseRedirect(
                    reverse(
                        redirect_url,
                        kwargs={
                            'tuiter_username': parameter_value
                        }
                    )
                )
        else:
            return HttpResponseRedirect(
                    reverse(redirect_url)
                )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def retuit(request):
    """Retuit Function."""
    if request.POST and request.user.is_authenticated:
        tuit_id = request.POST['tuit_id']
        redirect_url = request.POST['redirect_url']
        use_parameters = request.POST['use_parameters']
        user = request.user
        tuit = Tuit.objects.get(pk=tuit_id)
        if tuit.is_retuit:
            tuit = Tuit.objects.get(pk=tuit.original_tuit.id)
        newT = Tuit()
        newT.user = user
        newT.message = tuit.message
        newT.is_retuit = True
        newT.original_tuit = tuit
        newT.save()

        tuit.total_retuits = tuit.total_retuits+1
        tuit.save()

        if use_parameters == 'True':
            parameter_value = request.POST['parameter_value']
            return HttpResponseRedirect(
                    reverse(
                        redirect_url,
                        kwargs={
                            'tuiter_username': parameter_value
                        }
                    )
                )
        else:
            return HttpResponseRedirect(
                    reverse(redirect_url)
                )
    else:
        return render_to_response(
            'account/landing.html',
            context_instance=RequestContext(request)
        )


def uploadProfileImage(request):
    """Upload profile Function."""
    if request.POST and request.user.is_authenticated:
        user = request.user
        user_settings = UserSettings.objects.get(user=user)
        try:
            profile_picture = request.FILES['fileToUpload']
            user_settings.profile_picture = profile_picture
            user_settings.save()
            profileImageMessage = 'Image upload successful!'
            ctxt = {
                'profileImageMessage': profileImageMessage,
                'user': user,
                'user_settings': user_settings
            }
            return render_to_response(
                'tuits/edit_profile.html',
                context=ctxt,
                context_instance=RequestContext(request)
            )
        except:
            profileImageMessage = 'Error with image upload!'
            ctxt = {
                'profileImageMessage': profileImageMessage,
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


def uploadCoverImage(request):
    """Upload profile Function."""
    if request.POST and request.user.is_authenticated:
        user = request.user
        user_settings = UserSettings.objects.get(user=user)
        try:
            cover_picture = request.FILES['fileToUpload']
            user_settings.cover_picture = cover_picture
            user_settings.save()
            coverImageMessage = 'Image upload successful!'
            ctxt = {
                'coverImageMessage': coverImageMessage,
                'user': user,
                'user_settings': user_settings
            }
            return render_to_response(
                'tuits/edit_profile.html',
                context=ctxt,
                context_instance=RequestContext(request)
            )
        except:
            coverImageMessage = 'Error with image upload!'
            ctxt = {
                'coverImageMessage': coverImageMessage,
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
