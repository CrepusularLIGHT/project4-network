import datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


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
            username = "" ## <<<< THIS IS WHERE I LEFT OFF, get username
            # Extract content of post
            content = new_post_form.cleaned_data["content"]
            # Get current time
            time = datetime.datetime.now().strftime("%b/%d/%y %I:%M %p")
            # Number of likes
            likes = 0
            # Create the post 
            new_post = Post(username, content, time, likes)
            # Print to console
            print(new_post, new_post.username, new_post.content, new_post.time, new_post.likes)
            return render(request, "network/index.html", {
                "postForm": PostForm()
            })

    return render(request, "network/index.html", {
        "postForm": PostForm()
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

def following_view(request):
    return render(request, "network/following.html")

def profile_view(request, name):
    return render(request, "network/profile.html", {
        "name": name
    })