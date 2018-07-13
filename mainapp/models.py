from django.db import models
from tinymce.models import HTMLField


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=5, null=False)
    passwd = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=12, null=True)
    photo = models.ImageField(upload_to='photos')
    token = models.CharField(max_length=32,null=True)



class Blog(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(default='')
    content = HTMLField(default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cnt = models.IntegerField(default=0)


class Replay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    content = HTMLField(default='')
