from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# TODO: Here we need to discuss about fields
class Post(models.Model):
    objects = models.Manager()
    fileName = models.CharField(max_length=128)
    fileUrl = models.TextField()
    datePosted = models.DateTimeField(default=timezone.now)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fileName

