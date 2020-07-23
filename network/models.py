from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Include: Followers, following, posts
    pass

class Post(object):
    def __init__(self, username, content, time, likes):
        self.username = username
        self.content = content
        self.time = time
        self.likes = likes

    