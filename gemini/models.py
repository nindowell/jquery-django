from django.db import models
from django.conf import settings

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=300)
    title_ru = models.CharField(max_length=300, null=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Favorited(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorited_list')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
