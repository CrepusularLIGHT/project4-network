
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),
    path("profile/<str:name>", views.profile_view, name="profile"),
    path("follow/<str:user>/<str:user_to_follow>", views.follow, name="follow"),
    path("unfollow/<str:user>/<str:user_to_unfollow>", views.unfollow, name="unfollow"),
    path("like/<str:post>/<str:user>", views.like, name="like"),
    path("unlike/<str:post>/<str:user>", views.unlike, name="unlike")
]
