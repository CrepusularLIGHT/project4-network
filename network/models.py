from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    # Include: Followers, following, posts
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    content = models.TextField(max_length=64)
    time = models.DateTimeField(default=now)
    likes = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}: {self.content} -- {self.time} - likes: {self.likes}"

    