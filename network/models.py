from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    # following_count = models.IntegerField(default=0)
    # followers_count = models.IntegerField(default=0)

    # def add_follower(self, follower):
    #     self.followers_count = self.followers_count + 1
    #     return self.followers_count
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    content = models.TextField(max_length=64)
    time = models.DateTimeField(default=now)
    likes = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}: {self.content} -- {self.time} - likes: {self.likes}"

class Follower(models.Model):
    username = models.CharField(default='', max_length=150)
    following = models.ManyToManyField(User, blank=True, related_name="followers")