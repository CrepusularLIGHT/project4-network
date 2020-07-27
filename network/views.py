import datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Like, Follower, Following


# Form used to create NEW POST
class PostForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'new-post-textarea',
        'class': 'form-control',
        'name': 'new-post-textarea',
        'cols': 10,
        'rows': 3
    }))


def index(request):
    if request.method == "POST":
        # New post 
        new_post_form = PostForm(request.POST) #Gets info from form

        # Check if valid
        if new_post_form.is_valid():

            # Get username
            current_user = request.user

            # Extract content of post
            content = new_post_form.cleaned_data["content"]

            # Number of likes
            likes = 0 #Default value

            # Create the post 
            new_post = Post(user=current_user, content=content, likes=likes)
            new_post.save()
            print(new_post)

            # Function that returns list of post id's liked by user
            liked_post_id_list = likedPostList(request)

            return render(request, "network/index.html", {
                "postForm": PostForm(),
                "newPost": new_post,
                "posts": list(Post.objects.all().order_by('-time')),
                "liked_post_id_list": liked_post_id_list
            })
    
    # Function that returns list of post id's liked by user
    liked_post_id_list = likedPostList(request)

    return render(request, "network/index.html", {
        "postForm": PostForm(),
        "posts": list(Post.objects.all().order_by('-time')),
        "liked_post_id_list": liked_post_id_list
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile_view(request, name):
    user_info = User.objects.get(username=name)
    
    # Check if user is a follower
    # If following is True, render 'unfollow' button in HTML
    user_is_following = False   #Set for default value
    # Get all followers for user's profile
    followers = Follower.objects.filter(user__username=name).all()

    # From list of followers, check if logged in user exists in list
    for follower in followers:
        # If True, user is following
        if follower.follower == request.user.username:
            user_is_following = True
        # If name is not in list, user is not following
        else:
            user_is_following = False

    # Function that returns list of post id's liked by user
    liked_post_id_list = likedPostList(request)

    return render(request, "network/profile.html", {
        "name": user_info.username,
        "user_info": user_info,
        "user_is_following": user_is_following,
        "posts": list(Post.objects.all().filter(user__username=name)),
        "liked_post_id_list": liked_post_id_list
    })

def following_view(request):
    # Get all posts from following

    # List of all posts from newest to oldest
    all_posts = Post.objects.all().order_by('-time')

    # List to hold all posts from following
    following_posts = []
    
    # Get following list
    all_following = Following.objects.filter(user=request.user)
    all_following_list = list(all_following)

    # Loop through following list
    for following in all_following_list:
        username = following.following
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).all()
        for post in posts:
            following_posts.append(post)

    # Sort the posts from newest to oldest
    following_posts.sort(key=lambda x: x.time, reverse=True)

    # Function that returns list of post id's liked by user
    liked_post_id_list = likedPostList(request)

    return render(request, "network/following.html", {
        "posts": following_posts,
        "liked_post_id_list": liked_post_id_list
    })

def follow(request, user, user_to_follow):
    if request.method == "POST":
        # user1 follows user2

        # User objects
        user1 = User.objects.get(username=user)
        user2 = User.objects.get(username=user_to_follow)

        # Extract usernames
        user1_username = user1.username
        user2_username = user2.username

        ### ### ###
        # Follower
        ### ### ###

        # Create new follower object if it doesn't exist
        if Follower.objects.filter(follower=user1_username):
            follower_user = Follower.objects.get(follower=user1_username)
            follower_user.user.add(user2)
        else:
            follower_user = Follower(follower=user1_username)
            follower_user.save()
            follower_user.user.add(user2)

        # Get list of all followers
        all_followers = Follower.objects.filter(user=user2).all()
        all_followers_list = list(all_followers)
        print(user2_username, "FOLLOWERS:", all_followers_list)

        # Determine the number of followers from length of the list
        user2.followers_count = len(all_followers_list)
        user2.save()

        ### ### ###
        # Following
        ### ### ###

        # Create new following object if it doesn't exist
        if Following.objects.filter(following=user2_username):
            following_user = Following.objects.get(following=user2_username)
            following_user.user.add(user1)
        else:
            following_user = Following(following=user2_username)
            following_user.save()
            following_user.user.add(user1)

        # Get list of all following
        all_following = Following.objects.filter(user=user1).all()
        all_following_list = list(all_following)
        print(user1_username, "IS FOLLOWING:", all_following_list)

        # Determine the number following from length of the list
        user1.following_count = len(all_following_list)
        user1.save()

        return HttpResponseRedirect(reverse("profile", args=(user_to_follow,)))

def unfollow(request, user, user_to_unfollow):
    if request.method == "POST":
        # user1 unfollow user2

        # User objects
        user1 = User.objects.get(username=user)
        user2 = User.objects.get(username=user_to_unfollow)
        
        # Extract usernames
        user1_username = user1.username
        user2_username = user2.username

        ### ### ###
        # Follower
        ### ### ###

        # Get follower object and remove user2
        unfollow_user = Follower.objects.get(follower=user1_username, user=user2)
        unfollow_user.user.remove(user2)
        unfollow_user.save()

        # Get list of all followers
        all_followers = Follower.objects.filter(user=user2).all()
        all_followers_list = list(all_followers)
        print(user2_username, "FOLLOWERS:", all_followers_list)

        # Determine the number of followers from the length of the list
        user2.followers_count = len(all_followers_list)
        user2.save()

        ### ### ###
        # Following
        ### ### ###

        # Get following object and delete it
        unfollowing_user = Following.objects.get(following=user2_username, user=user1)
        unfollowing_user.user.remove(user1)
        unfollowing_user.save()

        # Get list of all following
        all_following = Following.objects.filter(user=user1).all()
        all_following_list = list(all_following)
        print(user1_username, "IS FOLLOWING:", all_following_list)

        # Determine the number of followers from the length of the list
        user1.following_count = len(all_following_list)
        user1.save()

        return HttpResponseRedirect(reverse("profile", args=(user_to_unfollow,)))


def like(request, post, user):
    """ 'user' likes 'post' """
    
    # Get post object
    post_to_like = Post.objects.get(pk=post)

    # Get user object
    user_that_likes = User.objects.get(username=user)
    
    # Create new like object if it doesn't exist
    if Like.objects.filter(post=post):
        like_post = Like.objects.get(post=post)
        like_post.user.add(user_that_likes)
        like_post.save()
    else:
        like_post = Like(post=post)
        like_post.save()
        like_post.user.add(user_that_likes)

    # Get list of all likes
    all_likes = Like.objects.get(post=post)
    all_likes_list = list(all_likes.user.all())

    # Determine the number of likes from the length of the list
    post_to_like.likes = len(all_likes_list)
    post_to_like.save()

    return redirect(request.META['HTTP_REFERER'])

def unlike(request, post, user):
    """ 'user' unlikes 'post' """

    # Get post object
    post_to_unlike = Post.objects.get(pk=post)

    # Get user object
    user_that_unlikes = User.objects.get(username=user)

    # Remove user from user list of Like object corresponding to post id
    unlike_post = Like.objects.get(post=post)
    unlike_post.user.remove(user_that_unlikes)
    unlike_post.save()

    # Get list of all likes
    all_likes = Like.objects.get(post=post)
    all_likes_list = list(all_likes.user.all())

    # Determine the number of likes from the length of the list
    post_to_unlike.likes = len(all_likes_list)
    post_to_unlike.save()

    return redirect(request.META['HTTP_REFERER'])


def likedPostList(request):
    """ Returns list of id's for liked posts """ 

    liked_post_id_list = []

    if request.user:
        liked_posts = Like.objects.filter(user=request.user).all()
        for post in liked_posts:
            liked_post_id_list.append(post.post)
    
    return liked_post_id_list