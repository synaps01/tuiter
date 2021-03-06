"""Urls for tuits."""

from django.conf.urls import url

from .views import tuits

urlpatterns = [
    url(r'^$', tuits.landingPageView, name='landing'),
    url(r'login$', tuits.tuiter_login, name='login'),
    url(r'register$', tuits.register, name='register'),
    url(r'logout$', tuits.tuiter_logout, name='logout'),
    url(r'timeline$', tuits.timeline, name='timeline'),
    url(r'newtuit$', tuits.newtuit, name='newtuit'),
    url(r'search_user$', tuits.searchUser, name='searchUser'),
    url(r'my_profile$', tuits.my_profile, name='my_profile'),
    url(r'edit_profile$', tuits.edit_profile, name='edit_profile'),
    url(r'edit_basic_info$', tuits.editBasicInfo, name='editBasicInfo'),
    url(r'change_password$', tuits.changePassword, name='changePassword'),
    url(r'delete_tuit$', tuits.deleteTuit, name='deleteTuit'),
    url(r'like_tuit$', tuits.likeTuit, name='likeTuit'),
    url(r'remove_tuit_like$', tuits.removeTuitLike, name='removeTuitLike'),
    url(r'retuit$', tuits.retuit, name='retuit'),
    url(
        r'user_profile/(?P<tuiter_username>[\w-]+)',
        tuits.userProfile,
        name='userProfile'
        ),
    url(
        r'user_follow/(?P<tuiter_user>[\w-]+)',
        tuits.userFollow,
        name='userFollow'
        ),
    url(
        r'user_unfollow/(?P<tuiter_user>[\w-]+)',
        tuits.userUnfollow,
        name='userUnfollow'
        ),
    url(
        r'user_following/(?P<tuiter_username>[\w-]+)',
        tuits.userProfileFollowing,
        name='userProfileFollowing'
        ),
    url(
        r'user_followers/(?P<tuiter_username>[\w-]+)',
        tuits.userProfileFollowers,
        name='userProfileFollowers'
        ),
    url(
        r'upload_profile_image$',
        tuits.uploadProfileImage,
        name='uploadProfileImage'
        ),
    url(
        r'upload_cover_image$',
        tuits.uploadCoverImage,
        name='uploadCoverImage'
        ),
    url(
        r'tuit_detail/(?P<tuit_id>[\d-]+)',
        tuits.tuitDetail,
        name='tuitDetail'
        ),
]
