from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    following_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)

    # def add_follower(self, follower):
    #     self.followers_count = self.followers_count + 1
    #     return self.followers_count


class Follower(models.Model):
    # 'follower' is following 'user'
    follower = models.CharField(default='', max_length=150)
    user = models.ManyToManyField(User, blank=True, related_name="user_followed")    
    
    def __str__(self):
        return self.follower
    

class Following(models.Model):
    # 'following' is followed by 'user'
    following = models.CharField(default='', max_length=150)
    user = models.ManyToManyField(User, blank=True, related_name="user_following")

    def __str__(self):
        return self.following
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    content = models.TextField(max_length=64, default="")
    time = models.DateTimeField(default=now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.content} -- {self.time} - likes: {self.likes}"
    

class Like(models.Model):
    post = models.IntegerField(default=0)
    user = models.ManyToManyField(User, blank=True, related_name="user_like")

    def __str__(self):
        return f"POST_ID: {self.post}"
