from django.contrib import admin

from .models import User, Post, Follower, Following, Like

# Register your models here.

class FollowerAdmin(admin.ModelAdmin):
    filter_horizontal = ("user",)

class FollowingAdmin(admin.ModelAdmin):
    filter_horizontal = ("user",)

class LikeAdmin(admin.ModelAdmin):
    filter_horizontal = ("user",)

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(Like, LikeAdmin)