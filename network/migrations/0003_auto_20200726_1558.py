# Generated by Django 3.0.7 on 2020-07-26 21:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20200725_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ManyToManyField(blank=True, related_name='post_like', to='network.Post'),
        ),
    ]